import cv2
import numpy as np
import time
import os
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler


class PictureReferenceMatcherError(Exception):
    pass


class CoarseFineChamferMatcher:

    def __init__(self,
                 pyramid_levels=3,
                 canny_low=50,
                 canny_high=150,
                 max_template_points=1500,
                 edge_mode="gradient",
                 edge_percentile=92.0,
                 ignore_border=2,
                 centered=None,
                 reference_keypoint=None,
                 coarse_angle_min=-45.0,
                 coarse_angle_max=45.0,
                 coarse_angle_step=5.0,
                 refine_angle_window=5.0,
                 refine_angle_step=1.0,
                 fine_angle_window=1.0,
                 fine_angle_step=0.2,
                 min_visible_fraction=0.90,
                 random_seed=0,
                 verbose=False):


        self.pyramid_levels = pyramid_levels
        self.canny_low = canny_low
        self.canny_high = canny_high
        self.max_template_points = max_template_points
        self.edge_mode = edge_mode
        self.edge_percentile = edge_percentile
        self.ignore_border = ignore_border
        self.centered = False
        self.reference_keypoint = reference_keypoint
        self.coarse_angle_min = coarse_angle_min
        self.coarse_angle_max = coarse_angle_max
        self.coarse_angle_step = coarse_angle_step
        self.refine_angle_window = refine_angle_window
        self.refine_angle_step = refine_angle_step
        self.fine_angle_window = fine_angle_window
        self.fine_angle_step = fine_angle_step
        self.min_visible_fraction = min_visible_fraction
        self.random_seed = random_seed
        self.verbose = verbose


    @staticmethod
    def _inclusive_angle_range(start, stop, step):

        start = float(start)
        stop = float(stop)
        step = float(step)

        if step <= 0:
            raise ValueError("Angle step must be > 0")
        if stop < start:
            raise ValueError("Angle range max must be >= min")

        return np.arange(start, stop + step * 0.5, step)


    def _coarse_angles(self):

        return self._inclusive_angle_range(
            self.coarse_angle_min,
            self.coarse_angle_max,
            self.coarse_angle_step
        )


    def _refine_angles(self, angle):

        return self._inclusive_angle_range(
            angle - self.refine_angle_window,
            angle + self.refine_angle_window,
            self.refine_angle_step
        )


    def _fine_angles(self, angle):

        return self._inclusive_angle_range(
            angle - self.fine_angle_window,
            angle + self.fine_angle_window,
            self.fine_angle_step
        )


    def create_pyramid(self, img):


        pyramid = [img]


        for _ in range(self.pyramid_levels - 1):
            img = cv2.pyrDown(img)
            pyramid.append(img)


        return pyramid[::-1]


    @staticmethod
    def load_image(path, verbose=True):


        if os.path.isfile(path):
            img = cv2.imread(path)
            if img is None:
                raise RuntimeError(
                    f"Failed to decode image: {path}"
                )
            return path, img


        base, _ext = os.path.splitext(path)
        for alt in [".bmp", ".png", ".jpg", ".jpeg", ".tif", ".tiff"]:
            cand = base + alt
            if os.path.isfile(cand):
                if verbose:
                    print(
                        f"  file not found: {path!r}; "
                        f"using: {cand!r}"
                    )
                img = cv2.imread(cand)
                if img is None:
                    raise RuntimeError(
                        f"Failed to decode image: {cand}"
                    )
                return cand, img


        raise FileNotFoundError(
            f"Image not found: {path!r} "
            f"(also tried .bmp/.png/.jpg/.jpeg/.tif/.tiff variants)"
        )


    def _to_gray(self, img):

        if len(img.shape) == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img


    def _gradient_magnitude(self, gray):


        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        mag = cv2.magnitude(gx, gy)


        hi = float(np.percentile(mag, self.edge_percentile))
        if hi <= 0:
            hi = 1.0

        edges = (mag >= hi).astype(np.uint8) * 255

        return edges


    def _edges(self, img):


        gray = self._to_gray(img)


        if self.edge_mode == "canny":
            return cv2.Canny(
                gray,
                self.canny_low,
                self.canny_high
            )


        return self._gradient_magnitude(gray)


    def edge_distance(self, img):

        edges = self._edges(img)

        distance = cv2.distanceTransform(
            255 - edges,
            cv2.DIST_L2,
            3
        )

        # Normalize by the image diagonal so the score
        # is a fraction of the image size, independent
        # of resolution and pyramid level.
        h, w = distance.shape
        diag = float(np.sqrt(h * h + w * w))
        if diag > 0:
            distance = distance / diag

        return distance


    def template_points(self, template):

        edges = self._edges(template)


        # Suppress border of the cropped image
        # (often picked up as a strong edge)
        if self.ignore_border > 0:
            edges[:self.ignore_border, :] = 0
            edges[-self.ignore_border:, :] = 0
            edges[:, :self.ignore_border] = 0
            edges[:, -self.ignore_border:] = 0

        pts = np.column_stack(
            np.where(edges > 0)
        )

        if len(pts) == 0:
            raise RuntimeError(
                "No template edges detected"
            )

        # y,x -> x,y
        pts = pts[:, ::-1]


        # Reduce points
        if len(pts) > self.max_template_points:

            rng = np.random.default_rng(
                self.random_seed
            )

            idx = rng.choice(
                len(pts),
                self.max_template_points,
                replace=False
            )

            pts = pts[idx]


        center = np.array([
            template.shape[1]/2,
            template.shape[0]/2
        ])


        return pts - center



    def rotate_points(self, pts, angle):

        a = np.deg2rad(angle)

        R = np.array([
            [np.cos(a), -np.sin(a)],
            [np.sin(a),  np.cos(a)]
        ])

        return pts @ R.T



    def evaluate_pose(self,
                      distance,
                      points,
                      x,
                      y):

        pts = np.round(
            points + np.array([x,y])
        ).astype(np.int32)


        h,w = distance.shape


        valid = (
            (pts[:,0] >= 0) &
            (pts[:,0] < w) &
            (pts[:,1] >= 0) &
            (pts[:,1] < h)
        )


        pts = pts[valid]


        min_valid = max(
            10,
            int(np.ceil(
                len(points) * self.min_visible_fraction
            ))
        )

        if len(pts) < min_valid:
            return np.inf


        return np.mean(
            distance[
                pts[:,1],
                pts[:,0]
            ]
        )


    def evaluate_pose_subpixel(self,
                               distance,
                               points,
                               x,
                               y):

        pts = points + np.array(
            [x, y],
            dtype=np.float32
        )

        h, w = distance.shape

        valid = (
            (pts[:, 0] >= 0) &
            (pts[:, 0] < w - 1) &
            (pts[:, 1] >= 0) &
            (pts[:, 1] < h - 1)
        )

        min_valid = max(
            10,
            int(np.ceil(
                len(points) * self.min_visible_fraction
            ))
        )

        if int(valid.sum()) < min_valid:
            return np.inf

        pts = pts[valid]

        x0 = np.floor(pts[:, 0]).astype(np.int32)
        y0 = np.floor(pts[:, 1]).astype(np.int32)
        dx = pts[:, 0] - x0
        dy = pts[:, 1] - y0

        v00 = distance[y0, x0]
        v10 = distance[y0, x0 + 1]
        v01 = distance[y0 + 1, x0]
        v11 = distance[y0 + 1, x0 + 1]

        vals = (
            v00 * (1.0 - dx) * (1.0 - dy) +
            v10 * dx * (1.0 - dy) +
            v01 * (1.0 - dx) * dy +
            v11 * dx * dy
        )

        return float(vals.mean())


    def refine_pose_subpixel(self,
                             distance,
                             template_pts,
                             pose):

        best_x, best_y, best_angle = pose
        rotated = self.rotate_points(
            template_pts,
            best_angle
        )
        best_score = self.evaluate_pose_subpixel(
            distance,
            rotated,
            best_x,
            best_y
        )

        passes = [
            (1.5, 0.25, 0.40, 0.05),
            (0.4, 0.10, 0.10, 0.02),
            (0.15, 0.05, 0.04, 0.01),
        ]

        for xy_radius, xy_step, angle_radius, angle_step in passes:

            cx, cy, ca = best_x, best_y, best_angle

            xs = np.arange(
                cx - xy_radius,
                cx + xy_radius + xy_step * 0.5,
                xy_step
            )
            ys = np.arange(
                cy - xy_radius,
                cy + xy_radius + xy_step * 0.5,
                xy_step
            )
            angles = np.arange(
                ca - angle_radius,
                ca + angle_radius + angle_step * 0.5,
                angle_step
            )

            for angle in angles:

                rotated = self.rotate_points(
                    template_pts,
                    angle
                )

                for y in ys:
                    for x in xs:

                        score = self.evaluate_pose_subpixel(
                            distance,
                            rotated,
                            x,
                            y
                        )

                        if score < best_score:
                            best_score = score
                            best_x = float(x)
                            best_y = float(y)
                            best_angle = float(angle)

        return (best_x, best_y, best_angle), best_score



    def search_level(self,
                     distance,
                     template_pts,
                     angles,
                     xy_step,
                     center=None,
                     window=None):


        h,w = distance.shape


        if center is None:

            x0,y0 = 0,0
            x1,y1 = w,h

        else:

            cx,cy = center

            x0 = max(
                0,
                int(cx-window)
            )

            x1 = min(
                w,
                int(cx+window)
            )

            y0 = max(
                0,
                int(cy-window)
            )

            y1 = min(
                h,
                int(cy+window)
            )


        xs = np.arange(
            x0,
            x1,
            xy_step,
            dtype=np.int32
        )

        ys = np.arange(
            y0,
            y1,
            xy_step,
            dtype=np.int32
        )


        if len(xs) == 0 or len(ys) == 0:
            return None, np.inf


        Xg, Yg = np.meshgrid(xs, ys)
        grid = np.column_stack([Xg.ravel(), Yg.ravel()]).astype(np.int32)
        M = grid.shape[0]


        N = template_pts.shape[0]
        min_valid = max(
            10,
            int(np.ceil(
                N * self.min_visible_fraction
            ))
        )
        rxs = np.empty((len(angles), N), dtype=np.int32)
        rys = np.empty((len(angles), N), dtype=np.int32)
        for i, a in enumerate(angles):
            r = self.rotate_points(template_pts, a)
            rxs[i] = np.round(r[:, 0]).astype(np.int32)
            rys[i] = np.round(r[:, 1]).astype(np.int32)


        best_score = np.inf
        best_pose = None


        BLOCK = 16384


        for i in range(len(angles)):

            rx = rxs[i]
            ry = rys[i]


            for k in range(0, M, BLOCK):

                block = grid[k:k + BLOCK]
                gx = block[:, 0][:, None]
                gy = block[:, 1][:, None]


                xs_idx = gx + rx[None, :]
                ys_idx = gy + ry[None, :]


                valid = (
                    (xs_idx >= 0) & (xs_idx < w) &
                    (ys_idx >= 0) & (ys_idx < h)
                )


                xs_c = np.clip(xs_idx, 0, w - 1)
                ys_c = np.clip(ys_idx, 0, h - 1)


                vals = distance[ys_c, xs_c]
                vals = np.where(valid, vals, 0.0)


                sums = vals.sum(axis=1)
                counts = valid.sum(axis=1)
                enough_visible = counts >= min_valid
                scores = np.where(
                    enough_visible,
                    sums / np.maximum(counts, 1),
                    np.inf
                )


                idx_local = int(np.argmin(scores))
                sc = float(scores[idx_local])
                if sc < best_score:
                    best_score = sc
                    best_pose = (int(block[idx_local, 0]),
                                 int(block[idx_local, 1]),
                                 float(angles[i]))


        return best_pose, best_score



    def set_images(self, template, image,
                   template_path=None, image_path=None):


        self.template = template
        self.image = image
        self.template_path = template_path
        self.image_path = image_path
        self.last_result = None
        return self


    def set_template_image(self, template, template_path=None):

        self.template = template
        self.template_path = template_path
        self.last_result = None
        return self


    def set_search_image(self, image, image_path=None):

        self.image = image
        self.image_path = image_path
        self.last_result = None
        return self


    def run(self, template_path, image_path,
            pyramid_levels=None, **kwargs):


        if pyramid_levels is not None:
            self.pyramid_levels = pyramid_levels

        tpl_path, template = self.load_image(template_path)
        img_path, image = self.load_image(image_path)

        self.set_images(
            template, image,
            template_path=tpl_path,
            image_path=img_path
        )

        result = self.match()
        return result, tpl_path, img_path


    def match(self, template=None, image=None):


        if template is None:
            template = self.template
        if image is None:
            image = self.image

        if template is None or image is None:
            raise ValueError(
                "No images set. Call set_images() first, "
                "or pass template and image to match()."
            )

        self.template = template
        self.image = image

        t0 = time.perf_counter()


        img_pyr = self.create_pyramid(
            image
        )

        tmp_pyr = self.create_pyramid(
            template
        )


        pose = None
        score = None



        for level in range(
            self.pyramid_levels
        ):


            if self.verbose:
                print(
                    f"\nLevel {level+1}/{self.pyramid_levels}"
                )


            img = img_pyr[level]
            tmp = tmp_pyr[level]


            distance = self.edge_distance(
                img
            )


            template_pts = self.template_points(
                tmp
            )


            scale = 2**(
                self.pyramid_levels-level-1
            )


            if pose is None:


                # coarse search

                angles = self._coarse_angles()


                pose,score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=8
                )


            else:


                # refine previous solution

                x,y,a = pose


                # previous pose is in the previous (smaller)
                # pyramid level's pixel coords; scale up to
                # this level's coords (2x per level step)
                x *= 2
                y *= 2


                angles = self._refine_angles(a)


                pose,score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=2,
                    center=(x,y),
                    window=40
                )


                # angle refinement

                x,y,a = pose


                angles = self._fine_angles(a)


                pose,score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=1,
                    center=(x,y),
                    window=10
                )


            if self.verbose:
                print(
                    "position:",
                    pose,
                    "score:",
                    score
                )


        pose, score = self.refine_pose_subpixel(
            distance,
            template_pts,
            pose
        )

        if self.verbose:
            print(
                "subpixel position:",
                pose,
                "score:",
                score
            )


        result = self._result_from_pose(pose, score, template, image)

        self.last_result = result


        if self.verbose:
            print(
                "\nFinished:",
                result,
                "time:",
                time.perf_counter()-t0,
                "s"
            )


        return result


    def match_near(self,
                   center_x,
                   center_y,
                   angle,
                   xy_window=100.0,
                   angle_window=5.0,
                   template=None,
                   image=None):

        if template is None:
            template = self.template
        if image is None:
            image = self.image

        if template is None or image is None:
            raise ValueError(
                "No images set. Call set_images() first, "
                "or pass template and image to match_near()."
            )

        old_coarse_min = self.coarse_angle_min
        old_coarse_max = self.coarse_angle_max
        old_refine_window = self.refine_angle_window
        old_fine_window = self.fine_angle_window

        try:
            self.coarse_angle_min = float(angle) - float(angle_window)
            self.coarse_angle_max = float(angle) + float(angle_window)
            self.refine_angle_window = min(float(self.refine_angle_window), float(angle_window))
            self.fine_angle_window = min(float(self.fine_angle_window), float(angle_window))
            return self._match_with_initial_pose(
                float(center_x),
                float(center_y),
                float(angle),
                float(xy_window),
                template=template,
                image=image,
            )
        finally:
            self.coarse_angle_min = old_coarse_min
            self.coarse_angle_max = old_coarse_max
            self.refine_angle_window = old_refine_window
            self.fine_angle_window = old_fine_window


    def _match_with_initial_pose(self,
                                 center_x,
                                 center_y,
                                 angle,
                                 xy_window,
                                 template=None,
                                 image=None):

        if template is None:
            template = self.template
        if image is None:
            image = self.image

        self.template = template
        self.image = image

        t0 = time.perf_counter()
        img_pyr = self.create_pyramid(image)
        tmp_pyr = self.create_pyramid(template)
        pose = None
        score = None

        for level in range(self.pyramid_levels):
            if self.verbose:
                print(f"\nLevel {level+1}/{self.pyramid_levels}")

            img = img_pyr[level]
            tmp = tmp_pyr[level]
            distance = self.edge_distance(img)
            template_pts = self.template_points(tmp)
            scale = 2**(self.pyramid_levels - level - 1)

            if pose is None:
                angles = self._inclusive_angle_range(
                    self.coarse_angle_min,
                    self.coarse_angle_max,
                    self.coarse_angle_step
                )
                pose, score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=max(1, min(8, int(np.ceil(float(xy_window) / max(scale, 1) / 8.0)))),
                    center=(center_x / scale, center_y / scale),
                    window=max(1.0, xy_window / scale)
                )
            else:
                x, y, a = pose
                x *= 2
                y *= 2
                angles = self._refine_angles(a)
                pose, score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=2,
                    center=(x, y),
                    window=max(5.0, xy_window / max(scale, 1))
                )

                x, y, a = pose
                angles = self._fine_angles(a)
                pose, score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=1,
                    center=(x, y),
                    window=10
                )

            if self.verbose:
                print("position:", pose, "score:", score)

        pose, score = self.refine_pose_subpixel(distance, template_pts, pose)

        if self.verbose:
            print("subpixel position:", pose, "score:", score)

        result = self._result_from_pose(pose, score, template, image)
        self.last_result = result

        if self.verbose:
            print("\nFinished:", result, "time:", time.perf_counter()-t0, "s")

        return result


    def _result_from_pose(self, pose, score, template, image):

        x, y, angle = pose

        ih, iw = image.shape[:2]
        th, tw = template.shape[:2]
        tpl_cx = tw / 2.0
        tpl_cy = th / 2.0
        if self.reference_keypoint is None:
            keypoint_x = tpl_cx
            keypoint_y = tpl_cy
        else:
            keypoint_x = float(self.reference_keypoint[0])
            keypoint_y = float(self.reference_keypoint[1])

        keypoint_x = float(np.clip(keypoint_x, 0.0, max(0.0, tw - 1.0)))
        keypoint_y = float(np.clip(keypoint_y, 0.0, max(0.0, th - 1.0)))

        a = np.deg2rad(angle)
        dx = keypoint_x - tpl_cx
        dy = keypoint_y - tpl_cy
        keypoint_abs_x = float(x) + dx * np.cos(a) - dy * np.sin(a)
        keypoint_abs_y = float(y) + dx * np.sin(a) + dy * np.cos(a)

        return {
            "x": keypoint_abs_x,
            "y": keypoint_abs_y,
            "angle": float(angle),
            "score": float(score),
            "x_abs": keypoint_abs_x,
            "y_abs": keypoint_abs_y,
            "template_center_x_abs": float(x),
            "template_center_y_abs": float(y),
            "reference_keypoint_x": keypoint_x,
            "reference_keypoint_y": keypoint_y,
            "centered": False,
            "image_size": (int(iw), int(ih)),
        }



    def verify(self,
               result=None,
               template=None,
               image=None,
               show=True,
               save_path=None,
               draw_contour=False,
               alpha=0.4,
               tint=None,
               thickness=2,
               cross=True,
               arrow=True,
               center_arrow=True,
               label=True):


        if result is None:
            result = getattr(self, "last_result", None)
        if result is None:
            raise ValueError(
                "No result available. Call match() first, "
                "or pass result to verify()."
            )


        if template is None:
            template = self.template
        if image is None:
            image = self.image

        if template is None or image is None:
            raise ValueError(
                "No template/image set. "
                "Call set_images() / match() first, "
                "or pass template and image to verify()."
            )


        if save_path is None and self.template_path and self.image_path:
            tpl_stem, _ = os.path.splitext(
                os.path.basename(self.template_path)
            )
            img_stem, _ = os.path.splitext(
                os.path.basename(self.image_path)
            )
            save_path = (
                f"verify_{tpl_stem}_in_{img_stem}.png"
            )


        # x_abs/y_abs are the configured reference keypoint. The template image
        # itself is drawn at the matched template center.
        if "x_abs" in result and "y_abs" in result:
            key_x = float(result["x_abs"])
            key_y = float(result["y_abs"])
        else:
            key_x = float(result["x"])
            key_y = float(result["y"])

        x = float(result.get("template_center_x_abs", key_x))
        y = float(result.get("template_center_y_abs", key_y))

        angle = float(result["angle"])
        score = float(result["score"])

        th, tw = template.shape[:2]
        ih, iw = image.shape[:2]


        canvas = image.copy()


        M = cv2.getRotationMatrix2D(
            (tw / 2.0, th / 2.0),
            -angle,
            1.0
        )


        rot_full = cv2.warpAffine(
            template,
            M,
            (tw, th),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )


        if rot_full.ndim == 2:
            rot_full = cv2.cvtColor(rot_full, cv2.COLOR_GRAY2BGR)


        x0 = int(round(x - tw / 2.0))
        y0 = int(round(y - th / 2.0))
        x1 = x0 + tw
        y1 = y0 + th

        sx0 = max(0, x0)
        sy0 = max(0, y0)
        sx1 = min(iw, x1)
        sy1 = min(ih, y1)


        if sx1 > sx0 and sy1 > sy0:

            rx0 = sx0 - x0
            ry0 = sy0 - y0
            rx1 = rx0 + (sx1 - sx0)
            ry1 = ry0 + (sy1 - sy0)

            patch = rot_full[ry0:ry1, rx0:rx1]


            if tint is not None:

                gray = (
                    cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
                    if patch.ndim == 3
                    else patch
                )

                tint_img = np.zeros_like(patch)
                tint_img[:] = tint

                mask = (gray > 0).astype(np.float32) * alpha
                mask3 = np.stack([mask] * 3, axis=-1)

                roi = canvas[sy0:sy1, sx0:sx1].astype(np.float32)
                blended = roi * (1.0 - mask3) + tint_img.astype(np.float32) * mask3
                canvas[sy0:sy1, sx0:sx1] = blended.astype(np.uint8)

            else:

                mask = (
                    np.any(patch > 0, axis=2)
                    if patch.ndim == 3
                    else patch > 0
                )

                mask_f = mask.astype(np.float32) * alpha

                roi = canvas[sy0:sy1, sx0:sx1].astype(np.float32)
                patch_f = patch.astype(np.float32)

                blended = roi.copy()
                blended[mask] = (
                    (1.0 - alpha) * roi[mask]
                    + alpha * patch_f[mask]
                )
                canvas[sy0:sy1, sx0:sx1] = blended.astype(np.uint8)


        if draw_contour:

            edges = self._edges(template)

            if self.ignore_border > 0:
                edges[:self.ignore_border, :] = 0
                edges[-self.ignore_border:, :] = 0
                edges[:, :self.ignore_border] = 0
                edges[:, -self.ignore_border:] = 0

            contours, _ = cv2.findContours(
                edges,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE
            )

            cx = tw / 2.0
            cy = th / 2.0
            a = np.deg2rad(angle)
            cos_a = np.cos(a)
            sin_a = np.sin(a)

            for cnt in contours:
                pts = cnt.reshape(-1, 2).astype(np.float32)
                px = pts[:, 0] - cx
                py = pts[:, 1] - cy
                rx = px * cos_a - py * sin_a
                ry = px * sin_a + py * cos_a
                shifted = np.column_stack([
                    rx + x,
                    ry + y
                ]).astype(np.int32)
                cv2.drawContours(
                    canvas,
                    [shifted],
                    -1,
                    (0, 255, 0),
                    thickness
                )


        if cross:

            cv2.drawMarker(
                canvas,
                (int(round(key_x)), int(round(key_y))),
                (0, 0, 255),
                markerType=cv2.MARKER_CROSS,
                markerSize=20,
                thickness=2
            )


        if center_arrow:


            cx_img = iw / 2.0
            cy_img = ih / 2.0

            cv2.circle(
                canvas,
                (int(round(cx_img)), int(round(cy_img))),
                6,
                (255, 255, 0),
                -1,
                cv2.LINE_AA
            )
            cv2.circle(
                canvas,
                (int(round(cx_img)), int(round(cy_img))),
                6,
                (0, 0, 0),
                1,
                cv2.LINE_AA
            )


            if abs(key_x - cx_img) > 1 or abs(key_y - cy_img) > 1:

                cv2.arrowedLine(
                    canvas,
                    (int(round(cx_img)), int(round(cy_img))),
                    (int(round(key_x)), int(round(key_y))),
                    (0, 255, 0),
                    2,
                    tipLength=0.1
                )


        if arrow:


            L = 0.35 * max(tw, th)

            a = np.deg2rad(angle)
            ex = int(round(key_x + L * np.cos(a)))
            ey = int(round(key_y + L * np.sin(a)))
            cv2.arrowedLine(
                canvas,
                (int(round(key_x)), int(round(key_y))),
                (ex, ey),
                (0, 0, 255),
                2,
                tipLength=0.25
            )


        if label:

            text = (
                f"x={key_x:.1f} y={key_y:.1f} "
                f"angle={angle:+.2f}  score={score:.3f}"
            )
            cv2.putText(
                canvas,
                text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
                cv2.LINE_AA
            )


        if save_path is not None:
            cv2.imwrite(save_path, canvas)
            print(f"  saved verification image to: {save_path}")

        if show:
            print(
                "  overlay: warped reference at matched pose "
                f"(keypoint x={key_x:.1f}, y={key_y:.1f} (abs), "
                f"angle={angle:+.2f}deg); "
                "red arrow = reference +x axis (orientation); "
                "green arrow = offset from image center to match"
            )
            cv2.imshow("verify", canvas)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        return canvas


    def draw_result_on_canvas(self,
                              canvas,
                              result=None,
                              template=None,
                              thickness=2,
                              border_color=(0, 165, 255),
                              draw_border=False,
                              **_unused_draw_options):
        """Draw the matched reference patch on a visual canvas."""

        if result is None:
            result = getattr(self, "last_result", None)
        if result is None:
            raise ValueError("No result available. Call match() first.")

        if template is None:
            template = self.template
        if template is None:
            raise ValueError("No template image available.")

        if len(canvas.shape) == 2:
            canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
        else:
            canvas = canvas.copy()

        x = float(result.get("template_center_x_abs", result["x_abs"]))
        y = float(result.get("template_center_y_abs", result["y_abs"]))
        angle = float(result["angle"])

        if template.ndim == 2:
            template_bgr = cv2.cvtColor(template, cv2.COLOR_GRAY2BGR)
            template_mask = np.full(template.shape[:2], 255, dtype=np.uint8)
        elif template.shape[2] == 4:
            template_bgr = template[:, :, :3].copy()
            template_mask = template[:, :, 3].copy()
        else:
            template_bgr = template.copy()
            template_mask = np.full(template.shape[:2], 255, dtype=np.uint8)

        th, tw = template_bgr.shape[:2]
        canvas_h, canvas_w = canvas.shape[:2]

        center = (tw / 2.0, th / 2.0)
        transform = cv2.getRotationMatrix2D(center, -angle, 1.0)
        transform[0, 2] += x - center[0]
        transform[1, 2] += y - center[1]

        warped_reference = cv2.warpAffine(
            template_bgr,
            transform,
            (canvas_w, canvas_h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )
        warped_mask = cv2.warpAffine(
            template_mask,
            transform,
            (canvas_w, canvas_h),
            flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )

        patch_pixels = warped_mask > 0
        canvas[patch_pixels] = warped_reference[patch_pixels]

        if not draw_border:
            return canvas

        corners = np.array(
            [[0, 0], [tw - 1, 0], [tw - 1, th - 1], [0, th - 1]],
            dtype=np.float32
        ).reshape(-1, 1, 2)
        transformed_corners = cv2.transform(corners, transform).astype(np.int32)
        cv2.polylines(
            canvas,
            [transformed_corners],
            True,
            border_color,
            max(1, int(thickness)),
            cv2.LINE_AA
        )

        return canvas


    def draw_reference_lines_on_canvas(self,
                                       canvas,
                                       result=None,
                                       template=None,
                                       thickness=2,
                                       roi_color=(0, 165, 255),
                                       x_axis_color=(0, 0, 255),
                                       y_axis_color=(0, 220, 0),
                                       **_unused_draw_options):
        """Draw matched ROI border and full-length keypoint cross."""

        if result is None:
            result = getattr(self, "last_result", None)
        if result is None:
            raise ValueError("No result available. Call match() first.")

        if template is None:
            template = self.template
        if template is None:
            raise ValueError("No template image available.")

        if len(canvas.shape) == 2:
            canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
        else:
            canvas = canvas.copy()

        x = float(result.get("template_center_x_abs", result["x_abs"]))
        y = float(result.get("template_center_y_abs", result["y_abs"]))
        angle = float(result["angle"])
        th, tw = template.shape[:2]

        keypoint_x = float(result.get("reference_keypoint_x", tw / 2.0))
        keypoint_y = float(result.get("reference_keypoint_y", th / 2.0))
        keypoint_x = float(np.clip(keypoint_x, 0.0, max(0.0, tw - 1.0)))
        keypoint_y = float(np.clip(keypoint_y, 0.0, max(0.0, th - 1.0)))

        center = (tw / 2.0, th / 2.0)
        transform = cv2.getRotationMatrix2D(center, -angle, 1.0)
        transform[0, 2] += x - center[0]
        transform[1, 2] += y - center[1]

        corners = np.array(
            [[0, 0], [tw - 1, 0], [tw - 1, th - 1], [0, th - 1]],
            dtype=np.float32
        ).reshape(-1, 1, 2)
        transformed_corners = cv2.transform(corners, transform).astype(np.int32)
        cv2.polylines(
            canvas,
            [transformed_corners],
            True,
            roi_color,
            max(1, int(thickness)),
            cv2.LINE_AA
        )

        horizontal = np.array(
            [[0, keypoint_y], [tw - 1, keypoint_y]],
            dtype=np.float32
        ).reshape(-1, 1, 2)
        vertical = np.array(
            [[keypoint_x, 0], [keypoint_x, th - 1]],
            dtype=np.float32
        ).reshape(-1, 1, 2)
        transformed_horizontal = cv2.transform(horizontal, transform).astype(np.int32)
        transformed_vertical = cv2.transform(vertical, transform).astype(np.int32)

        cv2.line(
            canvas,
            tuple(transformed_horizontal[0, 0]),
            tuple(transformed_horizontal[1, 0]),
            x_axis_color,
            max(1, int(thickness)),
            cv2.LINE_AA
        )
        cv2.line(
            canvas,
            tuple(transformed_vertical[0, 0]),
            tuple(transformed_vertical[1, 0]),
            y_axis_color,
            max(1, int(thickness)),
            cv2.LINE_AA
        )

        return canvas


def resolve_reference_image_path(process_file_path: str) -> str:

    if process_file_path in (None, ""):
        raise PictureReferenceMatcherError(
            "Process file path is not set; cannot locate matcher reference image."
        )

    process_path = Path(process_file_path)
    reference_base = process_path.parent / f"{process_path.stem}_matcher_reference_image"
    try:
        reference_path, _ = CoarseFineChamferMatcher.load_image(str(reference_base), verbose=False)
    except FileNotFoundError as exc:
        raise PictureReferenceMatcherError(
            "Matcher reference image not found. Expected a file next to the "
            f"vision process named '{reference_base.name}' with one of these "
            "extensions: .bmp, .png, .jpg, .jpeg, .tif, .tiff"
        ) from exc

    return reference_path


def resolve_reference_metadata_path(process_file_path: str) -> Path | None:

    if process_file_path in (None, ""):
        return None

    process_path = Path(process_file_path)
    reference_base = process_path.parent / f"{process_path.stem}_matcher_reference_image"
    metadata_path = process_path.parent / f"{reference_base.name}_metadata.json"
    return metadata_path if metadata_path.is_file() else None


def load_reference_metadata(process_file_path: str, logger=None) -> dict | None:

    metadata_path = resolve_reference_metadata_path(process_file_path)
    if metadata_path is None:
        return None

    try:
        with open(metadata_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        if logger:
            logger.warning(
                f"Could not read matcher reference metadata '{metadata_path}': {exc}."
            )
        return None


def load_reference_keypoint(process_file_path: str,
                            reference_image: np.ndarray,
                            logger=None) -> tuple[float, float]:

    height, width = reference_image.shape[:2]
    fallback = (width / 2.0, height / 2.0)
    metadata = load_reference_metadata(process_file_path, logger=logger)

    if metadata is None:
        return fallback

    keypoint = metadata.get("reference_keypoint_px")
    if not isinstance(keypoint, dict):
        settings = metadata.get("settings")
        if isinstance(settings, dict) and "keypoint_x_px" in settings and "keypoint_y_px" in settings:
            keypoint = {
                "x": settings.get("keypoint_x_px"),
                "y": settings.get("keypoint_y_px"),
            }

    if not isinstance(keypoint, dict):
        return fallback

    try:
        keypoint_x = float(keypoint["x"])
        keypoint_y = float(keypoint["y"])
    except (KeyError, TypeError, ValueError):
        if logger:
            logger.warning(
                "Invalid matcher reference keypoint. "
                "Using reference image center as keypoint."
            )
        return fallback

    return (
        float(np.clip(keypoint_x, 0.0, max(0.0, width - 1.0))),
        float(np.clip(keypoint_y, 0.0, max(0.0, height - 1.0))),
    )


def _rotation_matrix_bound(image_shape: tuple[int, ...], angle_deg: float) -> tuple[np.ndarray, tuple[int, int]]:

    h, w = image_shape[:2]
    center = (w / 2.0, h / 2.0)
    matrix = cv2.getRotationMatrix2D(center, angle_deg, 1.0)

    cos_v = abs(matrix[0, 0])
    sin_v = abs(matrix[0, 1])
    new_w = int((h * sin_v) + (w * cos_v))
    new_h = int((h * cos_v) + (w * sin_v))

    matrix[0, 2] += (new_w / 2.0) - center[0]
    matrix[1, 2] += (new_h / 2.0) - center[1]

    return matrix, (new_w, new_h)


def _source_shape_from_metadata(metadata: dict) -> tuple[int, int, int] | None:

    shape = metadata.get("source_image_shape")
    if isinstance(shape, dict) and "height" in shape and "width" in shape:
        return (
            int(shape["height"]),
            int(shape["width"]),
            int(shape.get("channels", 3)),
        )

    source_path = metadata.get("source_path")
    if source_path:
        image = cv2.imread(str(source_path), cv2.IMREAD_UNCHANGED)
        if image is not None:
            return image.shape

    return None


def metadata_pose_prior(process_file_path: str,
                        search_image_shape: tuple[int, ...],
                        roi_offset: tuple[float, float] = (0.0, 0.0),
                        logger=None) -> tuple[float, float, float] | None:

    metadata = load_reference_metadata(process_file_path, logger=logger)
    if metadata is None:
        return None

    settings = metadata.get("settings")
    if not isinstance(settings, dict):
        return None

    try:
        rotation_angle = float(settings.get("rotation_angle_deg", 0.0))
        roi_center_x = float(settings["roi_center_x"])
        roi_center_y = float(settings["roi_center_y"])
    except (KeyError, TypeError, ValueError):
        return None

    source_shape = _source_shape_from_metadata(metadata)
    if source_shape is None:
        if logger:
            logger.warning(
                "Matcher metadata pose prior unavailable: source image shape is missing."
            )
        return None

    matrix, _output_size = _rotation_matrix_bound(source_shape, rotation_angle)
    inverse = cv2.invertAffineTransform(matrix)
    source_center = inverse @ np.array(
        [roi_center_x, roi_center_y, 1.0],
        dtype=np.float64,
    )

    x = float(source_center[0]) - float(roi_offset[0])
    y = float(source_center[1]) - float(roi_offset[1])

    if not (0 <= x < search_image_shape[1] and 0 <= y < search_image_shape[0]):
        if logger:
            logger.warning(
                "Matcher metadata pose prior is outside the current search image; "
                "falling back to full-image search."
            )
        return None

    return x, y, -rotation_angle


def picture_reference_matcher(image_processing_handler: "ImageProcessingHandler",
                              pyramid_levels: int = 3,
                              canny_low: int = 50,
                              canny_high: int = 150,
                              max_template_points: int = 1500,
                              edge_mode: str = "gradient",
                              edge_percentile: float = 92.0,
                              ignore_border: int = 2,
                              coarse_angle_min: float = -45.0,
                              coarse_angle_max: float = 45.0,
                              coarse_angle_step: float = 5.0,
                              refine_angle_window: float = 5.0,
                              refine_angle_step: float = 1.0,
                              fine_angle_window: float = 1.0,
                              fine_angle_step: float = 0.2,
                              min_visible_fraction: float = 0.90,
                              random_seed: int = 0,
                              draw_match: bool = True,
                              draw_lines: bool = True,
                              use_metadata_pose_prior: bool = True,
                              metadata_pose_xy_window_px: float = 60.0,
                              metadata_pose_angle_window_deg: float = 1.0,
                              medium_score_threshold: float = 0.0005,
                              max_score_threshold: float = 0.0020,
                              verbose: bool = False,
                              logger=None):

    reference_path = resolve_reference_image_path(image_processing_handler.process_file_path)
    _, reference_image = CoarseFineChamferMatcher.load_image(reference_path, verbose=False)
    reference_keypoint = load_reference_keypoint(
        image_processing_handler.process_file_path,
        reference_image,
        logger=logger
    )
    search_image = image_processing_handler.get_processing_image()
    
    matcher = CoarseFineChamferMatcher(
        pyramid_levels=int(pyramid_levels),
        canny_low=int(canny_low),
        canny_high=int(canny_high),
        max_template_points=int(max_template_points),
        edge_mode=edge_mode,
        edge_percentile=float(edge_percentile),
        ignore_border=int(ignore_border),
        coarse_angle_min=float(coarse_angle_min),
        coarse_angle_max=float(coarse_angle_max),
        coarse_angle_step=float(coarse_angle_step),
        refine_angle_window=float(refine_angle_window),
        refine_angle_step=float(refine_angle_step),
        fine_angle_window=float(fine_angle_window),
        fine_angle_step=float(fine_angle_step),
        min_visible_fraction=float(min_visible_fraction),
        random_seed=int(random_seed),
        reference_keypoint=reference_keypoint,
        verbose=bool(verbose)
    )

    matcher.set_images(reference_image, search_image, template_path=reference_path)
    pose_prior = None
    if use_metadata_pose_prior:
        roi_offset = (0.0, 0.0)
        if getattr(image_processing_handler, "roi_used", False):
            roi_offset = (
                float(image_processing_handler.ROI_CS_CV_top_left_x),
                float(image_processing_handler.ROI_CS_CV_top_left_y),
            )
        pose_prior = metadata_pose_prior(
            image_processing_handler.process_file_path,
            search_image.shape,
            roi_offset=roi_offset,
            logger=logger,
        )

    if pose_prior is not None:
        result = matcher.match_near(
            center_x=pose_prior[0],
            center_y=pose_prior[1],
            angle=pose_prior[2],
            xy_window=float(metadata_pose_xy_window_px),
            angle_window=float(metadata_pose_angle_window_deg),
        )
    else:
        result = matcher.match()

    x = float(result["x_abs"])
    y = float(result["y_abs"])
    x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x, y)

    point = image_processing_handler.new_vision_point_result()
    point.axis_value_1 = x_cs_camera
    point.axis_value_2 = y_cs_camera
    point.axis_suffix_1 = image_processing_handler.camera_axis_1
    point.axis_suffix_2 = image_processing_handler.camera_axis_2
    point.angle = float(result["angle"])
    image_processing_handler.append_vision_obj_to_results(point)

    image_processing_handler.append_vision_process_debug(
        "PictureReferenceMatcher: "
        f"reference='{Path(reference_path).name}', "
        f"x={x:.2f}px, y={y:.2f}px, "
        f"angle={result['angle']:.3f}deg, score={result['score']:.6f}, "
        f"metadata_pose_prior={'used' if pose_prior is not None else 'not used'}"
    )

    score = float(result["score"])
    match_ok = True
    fit_quality = "good"
    if score > float(max_score_threshold):
        message = (
            "PictureReferenceMatcher failed: "
            f"score={score:.6f} exceeds max_score_threshold={float(max_score_threshold):.6f}"
        )
        if logger:
            logger.warn(message)
        image_processing_handler.append_vision_process_debug(message)
        match_ok = False
        fit_quality = "failed"

    elif score > float(medium_score_threshold):
        message = (
            "PictureReferenceMatcher medium fit: "
            f"score={score:.6f} exceeds medium_score_threshold={float(medium_score_threshold):.6f}"
        )
        if logger:
            logger.warn(message)
        image_processing_handler.append_vision_process_debug(message)
        fit_quality = "medium"

    image_processing_handler.set_quality_scores(
        "PictureReferenceMatcher",
        {
            "score": score,
            "medium_score_threshold": float(medium_score_threshold),
            "max_score_threshold": float(max_score_threshold),
            "fit_quality": fit_quality,
            "lower_score_is_better": True,
        }
    )

    if draw_match or draw_lines:
        canvas = image_processing_handler.get_visual_elements_canvas()
        thickness = image_processing_handler.img_height // 300 + 1
        if draw_match:
            canvas = matcher.draw_result_on_canvas(
                canvas,
                result=result,
                template=reference_image,
                thickness=thickness
            )
        if draw_lines:
            canvas = matcher.draw_reference_lines_on_canvas(
                canvas,
                result=result,
                template=reference_image,
                thickness=1
            )
        image_processing_handler.apply_visual_elements_canvas(canvas)

    image_processing_handler.set_vision_ok(match_ok)
    return result
