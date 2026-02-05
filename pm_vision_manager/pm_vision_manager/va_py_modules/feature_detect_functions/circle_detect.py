# Import the necessary libraries
import cv2 # OpenCV library
import numpy as np
import os
from math import pi                              
from pm_vision_manager.va_py_modules.vision_utils import rotate_image
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler, ImageNotBinaryError, ImageNotGrayScaleError

from circle_fit import circle_fit

def circleDetection(image_processing_handler: ImageProcessingHandler,
                    max_radius: float,
                    min_radius: float,  
                    circle_fit_mode:str, 
                    mode:str,
                    fit_single_circle: bool,
                    draw_circles: bool,
                    logger = None):
    
    if not image_processing_handler.is_process_image_binary():
        raise ImageNotBinaryError()
  
    frame_processed = image_processing_handler.get_processing_image()

    canvas = image_processing_handler.get_visual_elements_canvas()

    # Select mode
    mode_map = {
        "RETR_EXTERNAL": cv2.RETR_EXTERNAL,
        "RETR_LIST": cv2.RETR_LIST,
        "RETR_CCOMP": cv2.RETR_CCOMP,
        "RETR_TREE": cv2.RETR_TREE,
        "RETR_FLOODFILL": cv2.RETR_FLOODFILL
    }
    if mode not in mode_map:
        raise ValueError("Invalid mode: " + mode)
    mode_val = mode_map[mode]

    # Select method
    method_map = {
        "CHAIN_APPROX_SIMPLE": cv2.CHAIN_APPROX_SIMPLE,
        "CHAIN_APPROX_NONE": cv2.CHAIN_APPROX_NONE,
        "CHAIN_APPROX_TC89_L1": cv2.CHAIN_APPROX_TC89_L1,
        "CHAIN_APPROX_TC89_KCOS": cv2.CHAIN_APPROX_TC89_KCOS
    }

    method = "CHAIN_APPROX_NONE"

    if method not in method_map:
        raise ValueError("Invalid method: " + method)
    
    method_val = method_map[method]
    
    # Do a contour detection
    contours, hierarchy = cv2.findContours(frame_processed, 
                                   mode_val, 
                                   method_val)


    if hierarchy is None:
        image_processing_handler.set_vision_ok(False)
        return

    hierarchy = hierarchy[0]  # <-- REQUIRED

    if contours == []:
        if logger:
            logger.warn("No contours found")
        image_processing_handler.set_vision_ok(False)
        return

    found_circles_x = []
    found_circles_y = []
    found_circles_r = []
    found_circles_s = []
    found_circles_r_um = []
    
    all_point_coordinates = []

    # -------------------------
    # Remove points that touch the image border
    # -------------------------
    margin = 4  # number of pixels from edge to ignore
    h, w = frame_processed.shape[:2]

    filtered_contours = []

    for contour in contours:
        filtered_points = []
        for pt in contour:
            x, y = pt[0]
            # Only keep points not too close to the border
            if margin <= x < (w - margin) and margin <= y < (h - margin):
                filtered_points.append([[x, y]])
            # else:
            #     if logger:
            #         logger.warn(f"Point at border removed: ({x}, {y})")
        if filtered_points:
            filtered_contours.append(np.array(filtered_points, dtype=np.int32))

    contours = filtered_contours

    # -------------------------
    # Process contours
    # -------------------------
    for index, contour in enumerate(contours):

        if index >= 100:
            if logger:
                logger.warn("More than 100 contours found. Only first 100 processed")
            break

        points = []
        for pt in contour:
            x, y = pt[0]
            points.append([x, y])

        if len(points) < 4:
            continue

        if fit_single_circle:
            all_point_coordinates.extend(points)
            continue

        try:
            x, y, r, s = fit_circle(points, circle_fit_mode)
        except ValueError:
            continue

        radius_um = r * image_processing_handler.umPROpixel

        if min_radius < radius_um < max_radius:
            found_circles_x.append(x)
            found_circles_y.append(y)
            found_circles_r.append(r)
            found_circles_r_um.append(radius_um)
            found_circles_s.append(s)

    # -------------------------
    # Single-circle fitting
    # -------------------------
    if fit_single_circle:

        try:
            x, y, r, s = fit_circle(all_point_coordinates, circle_fit_mode)
        except ValueError:
            if logger:
                logger.warn("Not enough points for single-circle fit")
            image_processing_handler.set_vision_ok(False)
            return

        radius_um = r * image_processing_handler.umPROpixel

        if not (min_radius < radius_um < max_radius):
            if logger:
                logger.warn("Single fitted circle radius out of range")
            image_processing_handler.set_vision_ok(False)
            return

        found_circles_x = [x]
        found_circles_y = [y]
        found_circles_r = [r]
        found_circles_r_um = [radius_um]
        found_circles_s = [s]

    if len(found_circles_x) == 0:
        if logger:
            logger.warn("No circles found")
            image_processing_handler.append_vision_process_debug("No circles found")
        image_processing_handler.set_vision_ok(False)
        return
    
    for x, y, r, s, r_um in zip(found_circles_x, found_circles_y, found_circles_r, found_circles_s, found_circles_r_um):

        x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x, y)
   
        circle = image_processing_handler.new_vision_circle_result()
        circle.radius = r_um
        circle.center_point.axis_value_1 = x_cs_camera
        circle.center_point.axis_value_2 = y_cs_camera
        circle.center_point.axis_suffix_1 = image_processing_handler.camera_axis_1
        circle.center_point.axis_suffix_2 = image_processing_handler.camera_axis_2

        image_processing_handler.append_vision_obj_to_results(circle)
    
    image_processing_handler.set_vision_ok(True)
    
    line_size = image_processing_handler.img_height // 200 + 1

    # # Optional: draw all contour points
    # for contour in filtered_contours:
    #     for pt in contour:
    #         x, y = pt[0]
    #         cv2.circle(canvas, (x, y), radius=1, color=(255, 0, 0), thickness=-1)  # Blue dot

    if draw_circles:

        # Draw the circumference of the circle.
        for ind in range(len(found_circles_x)):
            x_tl_roi = found_circles_x[ind]
            y_tl_roi = found_circles_y[ind]
            radius = found_circles_r[ind]
            cv2.circle(canvas, (int(x_tl_roi), int(y_tl_roi)), int(round(radius)), (0, 255, 0), line_size)
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(canvas, (int(x_tl_roi), int(y_tl_roi)), 1, (0, 0, 255), line_size)

        image_processing_handler.apply_visual_elements_canvas(canvas)



def fit_circle(points, mode: str):
    """
    Fit a circle to a list of [x, y] points.

    Returns:
        x, y, r, s
    """
    if len(points) < 4:
        raise ValueError("Not enough points to fit a circle")

    match mode:
        case 'taubinSVD':
            return circle_fit.taubinSVD(points)
        case 'hyperSVD':
            return circle_fit.hyperSVD(points)
        case 'prattSVD':
            return circle_fit.prattSVD(points)
        case 'lm':
            return circle_fit.lm(points)
        case 'riemannSWFLa':
            return circle_fit.riemannSWFLa(points)
        case 'kmh':
            return circle_fit.kmh(points)
        case 'hyperLSQ':
            return circle_fit.hyperLSQ(points)
        case _:
            return circle_fit.standardLSQ(points)
