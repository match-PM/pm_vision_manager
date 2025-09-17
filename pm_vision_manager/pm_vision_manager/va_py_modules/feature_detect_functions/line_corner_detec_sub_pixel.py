# Import the necessary libraries
import cv2  # OpenCV library
import numpy as np
import os
from math import pi
from pm_vision_manager.va_py_modules import image_processing_handler
from pm_vision_manager.va_py_modules.vision_utils import rotate_image
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler, ImageNotBinaryError, ImageNotGrayScaleError


def _compute_edges(gray, sigma=1.0, t1=50, t2=150, aperture=3):
    """Slightly smooth, then Canny. No binarization needed."""
    if sigma and sigma > 0:
        gray = cv2.GaussianBlur(gray, (0, 0), sigmaX=sigma, sigmaY=sigma)
    edges = cv2.Canny(gray, t1, t2, apertureSize=aperture, L2gradient=True)
    return edges

def _sobel_gradients(gray):
    """sobel gradients and magnitude (float32)."""
    Ix = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    Iy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(Ix, Iy)
    return Ix, Iy, mag

def _bilinear_at(img, x, y):
    """
    Bilinear sampling of a single-channel float32 map at (x, y).
    img.shape = (H,W). Returns float.
    """
    h, w = img.shape[:2]
    if x < 0 or y < 0 or x > w - 1 or y > h - 1:
        x = np.clip(x, 0, w - 1)
        y = np.clip(y, 0, h - 1)

    x0 = int(np.floor(x))
    x1 = min(x0 + 1, w - 1)
    y0 = int(np.floor(y))
    y1 = min(y0 + 1, h - 1)

    dx = x - x0
    dy = y - y0

    v00 = img[y0, x0]
    v01 = img[y0, x1]
    v10 = img[y1, x0]
    v11 = img[y1, x1]

    v0 = v00 * (1 - dx) + v01 * dx
    v1 = v10 * (1 - dx) + v11 * dx
    return float(v0 * (1 - dy) + v1 * dy)

def _subpixel_refine_points_along_normal(pts, Ix, Iy, response_map, step=1.0, mag_eps=1e-6):
    """
    Refines each point p along the local normal n = grad / ||grad||.
    Uses 1D quadratic interpolation of the 'response_map' (e.g., gradient magnitude).
    Returns: refined points as float32 (N,2)
    """
    H, W = response_map.shape[:2]
    refined = []
    for (x, y) in pts:
        gx = _bilinear_at(Ix, x, y)
        gy = _bilinear_at(Iy, x, y)
        gnorm = np.hypot(gx, gy)

        if gnorm < mag_eps:
            refined.append([x, y])
            continue

        nx = gx / gnorm
        ny = gy / gnorm

        f0 = _bilinear_at(response_map, x, y)
        fm = _bilinear_at(response_map, x - step * nx, y - step * ny)
        fp = _bilinear_at(response_map, x + step * nx, y + step * ny)

        denom = 2.0 * (fm - 2.0 * f0 + fp)
        if abs(denom) < 1e-6:
            refined.append([x, y])
            continue

        delta = (fm - fp) / denom
        if not np.isfinite(delta):
            delta = 0.0
        delta = float(np.clip(delta, -1.5, 1.5))

        xr = float(np.clip(x + delta * nx, 0, W - 1))
        yr = float(np.clip(y + delta * ny, 0, H - 1))

        refined.append([xr, yr])

    return np.array(refined, dtype=np.float32)

# ---- helpers for compact quality scoring ----

def _window_median(img, x, y, r=5):
    h, w = img.shape[:2]
    xi, yi = int(np.floor(x)), int(np.floor(y))
    x0 = max(xi - r, 0); x1 = min(xi + r + 1, w)
    y0 = max(yi - r, 0); y1 = min(yi + r + 1, h)
    if x1 <= x0 or y1 <= y0:
        return 0.0
    return float(np.median(img[y0:y1, x0:x1]))

def _calculate_intersection_homography(seg1_xyxy, seg2_xyxy):
    # robust line intersection in homogeneous coords
    x1, y1, x2, y2 = seg1_xyxy
    x3, y3, x4, y4 = seg2_xyxy
    L1 = np.cross(np.array([x1, y1, 1.0]), np.array([x2, y2, 1.0]))
    L2 = np.cross(np.array([x3, y3, 1.0]), np.array([x4, y4, 1.0]))
    X = np.cross(L1, L2)
    if abs(X[2]) < 1e-9:
        return None
    return float(X[0]/X[2]), float(X[1]/X[2])


def _corner_quality(meta1, meta2, *, R0=0.75, alpha=0.30, N0_min=20, N0_max=10000):
    """
    Compute compact sub-scores (no overall score, no angle subscore) and
    return the inter-line angle G in [0..180] degrees.

    Subscores (0..100, higher is better):
      - resid: 1 when residuals << R0 px; 0 when >= R0 px
      - inliers: normalized by N0 = clamp(alpha * min(line_length_px), N0_min..N0_max)

    Returns:
      P : [int resid, int inliers]
      G : int inter-line angle in degrees [0..180]
    """
    # residual term (pixels)
    worst_resid = max(meta1["residual_median"], meta2["residual_median"])
    q_resid = float(np.clip(1.0 - worst_resid * 2.2 / R0, 0.0, 1.0))

    # inlier term (points), with length-adaptive N0
    L_eff = max(1.0, min(meta1["length_px"], meta2["length_px"]))  # use the shorter segment
    N0 = float(np.clip(alpha * L_eff, N0_min, N0_max))
    best_inliers = min(meta1["inliers"], meta2["inliers"])
    q_inliers = float(np.clip(best_inliers / N0, 0.0, 1.0))

    # inter-line angle (0..180) using directed vectors (no abs on dot)
    dot = float(meta1["v"] @ meta2["v"])
    dot = np.clip(dot, -1.0, 1.0)
    G = int(round(np.degrees(np.arccos(dot))))  # 0..180

    P = [int(round(100*q_resid)), int(round(100*q_inliers))]
    return P, G


# -----------------------------------------------------------

def _refine_line_with_fitLine(edges, line_xyxy, gray, dist_thresh=2.5, min_inliers=10):
    """
    Refines the Hough segment with subpixel accuracy (returns segment and meta).
    """
    h, w = edges.shape[:2]
    x1, y1, x2, y2 = [float(v) for v in line_xyxy]

    seg_vec = np.array([x2 - x1, y2 - y1], dtype=np.float32)
    seg_len = np.linalg.norm(seg_vec) + 1e-9
    dir_unit = seg_vec / seg_len
    nrm_unit = np.array([-dir_unit[1], dir_unit[0]], dtype=np.float32)

    ys, xs = np.nonzero(edges)
    if len(xs) == 0:
        seg = np.array([[x1, y1, x2, y2]], dtype=np.float32)
        meta = {"v": dir_unit, "p": np.array([x1, y1], np.float32),
                "inliers": 0, "residual_median": 1e9,
                "t_min": 0.0, "t_max": 0.0, "length_px": seg_len}
        return seg, meta

    pts = np.column_stack([xs.astype(np.float32), ys.astype(np.float32)])
    p0 = np.array([x1, y1], dtype=np.float32)
    dists = (pts - p0) @ nrm_unit
    inliers = pts[np.abs(dists) <= dist_thresh]
    if len(inliers) < min_inliers:
        seg = np.array([[x1, y1, x2, y2]], dtype=np.float32)
        meta = {"v": dir_unit, "p": p0,
                "inliers": int(len(inliers)), "residual_median": 1e9,
                "t_min": 0.0, "t_max": 0.0, "length_px": seg_len}
        return seg, meta

    Ix, Iy, mag = _sobel_gradients(gray)

    inliers_refined = _subpixel_refine_points_along_normal(
        inliers, Ix, Iy, response_map=mag, step=1.0, mag_eps=1e-6
    )

    vx, vy, x0, y0 = cv2.fitLine(inliers_refined, cv2.DIST_L2, 0, 0.01, 0.01)
    v = np.array([float(vx), float(vy)], dtype=np.float32)
    v /= (np.linalg.norm(v) + 1e-9)
    p = np.array([float(x0), float(y0)], dtype=np.float32)

    t_vals = (inliers_refined - p) @ v
    t_min, t_max = float(np.min(t_vals)), float(np.max(t_vals))
    p1 = p + t_min * v
    p2 = p + t_max * v

    def _clip_point(P):
        return np.array([np.clip(P[0], 0, w - 1), np.clip(P[1], 0, h - 1)], dtype=np.float32)

    p1c = _clip_point(p1)
    p2c = _clip_point(p2)

    n = np.array([-v[1], v[0]], dtype=np.float32)
    residuals = np.abs((inliers_refined - p) @ n)
    residual_median = float(np.median(residuals)) if residuals.size else 1e9
    length_px = float(t_max - t_min)

    seg = np.array([[p1c[0], p1c[1], p2c[0], p2c[1]]], dtype=np.float32)
    meta = {
        "v": v, "p": p,
        "inliers": int(len(inliers_refined)),
        "residual_median": residual_median,
        "t_min": float(t_min), "t_max": float(t_max),
        "length_px": length_px
    }
    return seg, meta


def fitLine_pre(image_processing_handler: ImageProcessingHandler, line_selection: str, search_accuracy: str, minLineLength:int, dist_thresh: float, min_inliers: int, logger = None):
    frame_processed = image_processing_handler.get_processing_image()
    if not image_processing_handler.is_process_image_grayscale():
        raise ImageNotGrayScaleError()

    apertureSize = 3
    t1 = 50
    t2 = 150

    edges = cv2.Canny(frame_processed, 
                      threshold1=t1, 
                      threshold2=t2, 
                      apertureSize=apertureSize, 
                      L2gradient=True)

    minLineLength_pix = int(image_processing_handler.pixelPROum * minLineLength)
    threshold_adaptive = max(10, int(0.2 * minLineLength_pix)) 
    maxLineGap_adaptive = max(2, int(0.25 * minLineLength_pix))

    match search_accuracy:
        case "coarse":
            rho_adaptive = 1.0
            theta_adaptive = 180
        case "fine":
            rho_adaptive = 0.5
            theta_adaptive = 1800
        case "finest":
            rho_adaptive = 0.5
            theta_adaptive = 3600
        case "max_limit":
            rho_adaptive = 0.5
            theta_adaptive = 16400
        case _:
            rho_adaptive = 1.0
            theta_adaptive = 180

    lines = cv2.HoughLinesP(
        edges,
        rho=rho_adaptive,
        theta=np.pi / theta_adaptive,
        threshold=threshold_adaptive,
        minLineLength=minLineLength_pix,
        maxLineGap=maxLineGap_adaptive
    )

    canvas = image_processing_handler.get_visual_elements_canvas()

    if lines is not None:
        deltas_x = [abs(line[0][2] - line[0][0]) for line in lines]
        deltas_y = [abs(line[0][3] - line[0][1]) for line in lines]

        if logger:
            logger.debug(f"{(deltas_x)} are the deltas x!")
            logger.debug(f"{(deltas_y)} are the deltas y!")

        delta_deltas = [dx - dy for dx, dy in zip(deltas_x, deltas_y)]

        horizontal_lines_indicies = [idx for idx, value in enumerate(delta_deltas) if value >= 0]
        vertical_lines_indicies = [idx for idx, value in enumerate(delta_deltas) if value < 0]

        if logger:
            logger.debug(f"{(horizontal_lines_indicies)} are horizontal lines!")
            logger.debug(f"{(vertical_lines_indicies)} are vertical lines!")

        midpoints_horizontal = [((line[0][0] + line[0][2]) / 2, (line[0][1] + line[0][3]) / 2)
                                for idx, line in enumerate(lines) if idx in horizontal_lines_indicies]
        midpoints_vertical = [((line[0][0] + line[0][2]) / 2, (line[0][1] + line[0][3]) / 2)
                              for idx, line in enumerate(lines) if idx in vertical_lines_indicies]

        if logger:
            logger.debug(f"{(midpoints_horizontal)} are horizontal midpoints!")
            logger.debug(f"{(midpoints_vertical)} are vertical midpoints!")

        left_vert_mid_ind = []
        right_vert_mid_ind = []
        if midpoints_vertical:
            max_x_mid_vert = max(p[0] for p in midpoints_vertical)
            min_x_mid_vert = min(p[0] for p in midpoints_vertical)
            abs_x_mid_vert = abs(max_x_mid_vert + min_x_mid_vert) / 2

            if logger:
                logger.debug(f"{(max_x_mid_vert)} is max x mid vert!")
                logger.debug(f"{(min_x_mid_vert)} is min x mid vert!")
                logger.debug(f"{(abs_x_mid_vert)} is abs x mid vert!")

            left_vert_mid_ind = [ind for ind, p in enumerate(midpoints_vertical) if p[0] <= abs_x_mid_vert]
            right_vert_mid_ind = [ind for ind, p in enumerate(midpoints_vertical) if p[0] > abs_x_mid_vert]

        top_hor_mid_ind = []
        bottom_hor_mid_ind = []
        if midpoints_horizontal:
            max_y_mid_hor = max(p[1] for p in midpoints_horizontal)
            min_y_mid_hor = min(p[1] for p in midpoints_horizontal)
            abs_y_mid_hor = abs(max_y_mid_hor + min_y_mid_hor) / 2

            if logger:
                logger.debug(f"{(max_y_mid_hor)} is max y mid hor!")
                logger.debug(f"{(min_y_mid_hor)} is min y mid hor!")
                logger.debug(f"{(abs_y_mid_hor)} is abs y mid hor!")

            top_hor_mid_ind = [ind for ind, p in enumerate(midpoints_horizontal) if p[1] <= abs_y_mid_hor]
            bottom_hor_mid_ind = [ind for ind, p in enumerate(midpoints_horizontal) if p[1] > abs_y_mid_hor]

        selected_line = None

        if logger:
            logger.warn(f"Found {len(left_vert_mid_ind)} left vertical lines!")
            logger.warn(f"Found {len(right_vert_mid_ind)} right vertical lines!")
            logger.warn(f"Found {len(top_hor_mid_ind)} top horizontal lines!")
            logger.warn(f"Found {len(bottom_hor_mid_ind)} bottom horizontal lines!")

        match line_selection:
            case "left":
                if left_vert_mid_ind:
                    line_ind_left_vertical = vertical_lines_indicies[left_vert_mid_ind[0]]
                    selected_line = lines[line_ind_left_vertical]
                    image_processing_handler.append_vision_process_debug(f"Found {len(left_vert_mid_ind)} left vertical lines!")
                    if logger:
                        logger.error("Found line according to 'left' selection")
            case "right":
                if right_vert_mid_ind:
                    line_ind_right_vertical = vertical_lines_indicies[right_vert_mid_ind[0]]
                    selected_line = lines[line_ind_right_vertical]
                    image_processing_handler.append_vision_process_debug(f"Found {len(right_vert_mid_ind)} right vertical lines!")
                    if logger:
                        logger.error("Found line according to 'right' selection")
            case "top":
                if top_hor_mid_ind:
                    line_ind_top_horizontal = horizontal_lines_indicies[top_hor_mid_ind[0]]
                    selected_line = lines[line_ind_top_horizontal]
                    image_processing_handler.append_vision_process_debug(f"Found {len(top_hor_mid_ind)} top horizontal lines!")
                    if logger:
                        logger.error("Found line according to 'top' selection")
            case "bottom":
                if bottom_hor_mid_ind:
                    line_ind_bottom_horizontal = horizontal_lines_indicies[bottom_hor_mid_ind[0]]
                    selected_line = lines[line_ind_bottom_horizontal]
                    image_processing_handler.append_vision_process_debug(f"Found {len(bottom_hor_mid_ind)} bottom horizontal lines!")
                    if logger:
                        logger.error("Found line according to 'bottom' selection")

        if selected_line is not None:
            refined, meta = _refine_line_with_fitLine(edges, selected_line[0], frame_processed, dist_thresh=dist_thresh, min_inliers=min_inliers)
            return refined, meta  # refined shape (1,4), plus meta
        else:
            if logger:
                logger.error("No lines detected")
            image_processing_handler.append_vision_process_debug("No lines detected")
            return None
    else:
        if logger:
            logger.error("No lines detected. Hough lines found no lines")
        image_processing_handler.append_vision_process_debug("No lines detected. Hough lines found no lines")
        return None

def fitLine(image_processing_handler: ImageProcessingHandler, line_selection: str, search_accuracy: str, minLineLength:int, dist_thresh: float, min_inliers: int, logger = None):
    out = fitLine_pre(image_processing_handler, line_selection, search_accuracy, minLineLength, dist_thresh, min_inliers, logger)
    if out is None:
        image_processing_handler.set_vision_ok(False)
        return
    line, _meta = out

    canvas = image_processing_handler.get_visual_elements_canvas()

    x1, y1, x2, y2 = [float(v) for v in line[0]]

    cv2.line(canvas, (int(round(x1)), int(round(y1))), (int(round(x2)), int(round(y2))), (0, 255, 0), 2)

    x1_cs_camera, y1_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x1, y1)
    x2_cs_camera, y2_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x2, y2)

    line_length_um = float(np.hypot(x2_cs_camera - x1_cs_camera, y2_cs_camera - y1_cs_camera))
    # robust angle using atan2
    line_angle = float(np.arctan2((y2_cs_camera - y1_cs_camera), (x2_cs_camera - x1_cs_camera)) * 180 / pi)

    lobj = image_processing_handler.new_vision_line_result()
    lobj.point_1.axis_value_1 = x1_cs_camera
    lobj.point_1.axis_value_2 = y1_cs_camera
    lobj.point_1.axis_suffix_1 = image_processing_handler.camera_axis_1
    lobj.point_1.axis_suffix_2 = image_processing_handler.camera_axis_2
    lobj.point_2.axis_value_1 = x2_cs_camera
    lobj.point_2.axis_value_2 = y2_cs_camera
    lobj.point_2.axis_suffix_1 = image_processing_handler.camera_axis_1
    lobj.point_2.axis_suffix_2 = image_processing_handler.camera_axis_2
    lobj.point_mid.axis_suffix_1 = image_processing_handler.camera_axis_1
    lobj.point_mid.axis_suffix_2 = image_processing_handler.camera_axis_2
    lobj.point_mid.axis_value_1 = (x1_cs_camera + x2_cs_camera) / 2.0
    lobj.point_mid.axis_value_2 = (y1_cs_camera + y2_cs_camera) / 2.0
    lobj.length = line_length_um
    lobj.angle = line_angle

    image_processing_handler.apply_visual_elements_canvas(canvas)
    image_processing_handler.append_vision_obj_to_results(lobj)

def cornerDetectionSubPixel(image_processing_handler: ImageProcessingHandler,
                    line_1_selection: str,
                    line_2_selection: str,
                    search_accuracy: str,
                    minLineLength_1: float,
                    minLineLength_2: float,
                    dist_thresh: float = 1.5,
                    min_inliers: int = 10,
                    logger = None):
    '''
    Detect corner via intersection of two lines with compact quality payload.

    Returns (token-efficient):
      success: {"v":"c1","ok":1,"Q":int0-100,"P":[...5 ints...],"W":0-4,"A":"a|s|t|l|c"}
      failure: {"v":"c1","ok":0,"e":"same|l1|l2|par|oob"}
    '''
    if line_1_selection == line_2_selection:
        if logger: logger.error("Line 1 and Line 2 cannot be the same!")
        image_processing_handler.append_vision_process_debug("Line 1 and Line 2 cannot be the same!")
        image_processing_handler.set_vision_ok(False)
        return 

    out1 = fitLine_pre(image_processing_handler, line_1_selection, search_accuracy, minLineLength_1, dist_thresh, min_inliers, logger=logger)
    if out1 is None:
        if logger: logger.error("No line for input 1 detected")
        image_processing_handler.append_vision_process_debug("No line for input 1 detected")
        image_processing_handler.set_vision_ok(False)
        return

    line_1, meta_1 = out1
    canvas = image_processing_handler.get_visual_elements_canvas()
    l1x1, l1y1, l1x2, l1y2 = [float(v) for v in line_1[0]]
    cv2.line(canvas, (int(round(l1x1)), int(round(l1y1))), (int(round(l1x2)), int(round(l1y2))), (0, 255, 0), 2)

    out2 = fitLine_pre(image_processing_handler, line_2_selection, search_accuracy, minLineLength_2, dist_thresh, min_inliers, logger=logger)
    if out2 is None:
        if logger: logger.error("No line for input 2 detected")
        image_processing_handler.append_vision_process_debug("No line for input 2 detected")
        image_processing_handler.set_vision_ok(False)
        return

    line_2, meta_2 = out2
    l2x1, l2y1, l2x2, l2y2 = [float(v) for v in line_2[0]]
    cv2.line(canvas, (int(round(l2x1)), int(round(l2y1))), (int(round(l2x2)), int(round(l2y2))), (0, 255, 0), 2)

    # robust intersection (pixel coords)
    inter = _calculate_intersection_homography(line_1[0], line_2[0])
    if inter is None:
        if logger: logger.error("No intersection point detected!")
        image_processing_handler.append_vision_process_debug("No intersection point detected!")
        image_processing_handler.set_vision_ok(False)
        return

    x, y = float(inter[0]), float(inter[1])

    h, w = image_processing_handler.get_processing_image().shape[:2]
    if x < 0 or x > w or y < 0 or y > h:
        if logger: logger.error("No valid point of intersection found!")
        image_processing_handler.append_vision_process_debug("No valid point of intersection found!")
        image_processing_handler.apply_visual_elements_canvas(canvas)
        image_processing_handler.set_vision_ok(False)
        return

    cv2.drawMarker(canvas, (int(round(x)), int(round(y))), (0, 0, 255),
                   markerType=cv2.MARKER_CROSS, markerSize=50, thickness=2)

    # quality computation 
    P, G = _corner_quality(meta_1, meta_2, R0=0.75, alpha=0.30, N0_min=20)

    # weakest subscore + action suggestion
    # indices: 0=resid, 1=inliers
    W = int(np.argmin(P))
    A = ["s","t"][W]  # s: more smoothing or larger dist_thresh; t: more inliers (lower Canny, increase maxLineGap, finer search)

    # convert to camera CS (side-effect only)
    x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x, y)
    if logger: logger.error(f"intersection {x_cs_camera}, {y_cs_camera}!")

    point = image_processing_handler.new_vision_point_result()
    point.axis_value_1 = x_cs_camera
    point.axis_value_2 = y_cs_camera
    point.axis_suffix_1 = image_processing_handler.camera_axis_1
    point.axis_suffix_2 = image_processing_handler.camera_axis_2
    image_processing_handler.append_vision_obj_to_results(point)
    image_processing_handler.apply_visual_elements_canvas(canvas)
    image_processing_handler.set_vision_ok(True)

    # minimal, token-efficient payload for the agent
    if logger: logger.info(f"Corner detected with quality {P}, weakest {W}:{A}, angle {G} deg")

    return

def calculate_intersection(line1, line2, logger=None):
    # kept for backward-compat but unused by the new corner path
    (x1, y1, x2, y2), (x3, y3, x4, y4) = line1[0], line2[0]
    if x1 == x2:
        m1 = None
    else:
        m1 = (y2 - y1) / (x2 - x1)
    if x3 == x4:
        m2 = None
    else:
        m2 = (y4 - y3) / (x4 - x3)
    if m1 is not None:
        c1 = y1 - m1 * x1
    else:
        c1 = None
    if m2 is not None:
        c2 = y3 - m2 * x3
    else:
        c2 = None
    if m1 == m2:
        return None
    elif m1 is None:
        x = x1
        y = m2 * x + c2
        return x, y
    elif m2 is None:
        x = x3
        y = m1 * x + c1
        return x, y
    else:
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1
        return x, y
