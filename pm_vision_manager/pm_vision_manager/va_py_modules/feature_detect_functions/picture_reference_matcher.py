import cv2
import json
import numpy as np
from pathlib import Path
from time import perf_counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler


class PictureReferenceMatcherError(RuntimeError):
    pass

class _ChamferSearchEngine:

    def __init__(self,
                 pyramid_levels=3,
                 max_template_points=1500,
                 edge_percentile=92.0,
                 ignore_border=2,
                 reference_keypoint=None,
                 coarse_angle_min=-45.0,
                 coarse_angle_max=45.0,
                 coarse_angle_step=5.0,
                 refine_angle_window=5.0,
                 refine_angle_step=1.0,
                 fine_angle_window=1.0,
                 fine_angle_step=0.2,
                 min_visible_fraction=0.90,
                 random_seed=0):

        self.pyramid_levels = pyramid_levels
        self.max_template_points = max_template_points
        self.edge_percentile = edge_percentile
        self.ignore_border = ignore_border
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
        # Temporary per-call state used only by match_feature().
        self._keypoint_focus_radius = 0.0

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

    def _to_gray(img):

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
        return self._gradient_magnitude(self._to_gray(img))

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

        edge_source = template
        offset_x = 0
        offset_y = 0
        if self._keypoint_focus_radius > 0 and self.reference_keypoint is not None:
            # Crop before edge extraction. In gradient-percentile mode this is
            # important: otherwise strong repetitive structures control the
            # global threshold and a smaller distinctive feature may disappear.
            full_h, full_w = self.template.shape[:2]
            scale_x = template.shape[1] / float(full_w)
            scale_y = template.shape[0] / float(full_h)
            keypoint_x = float(self.reference_keypoint[0]) * scale_x
            keypoint_y = float(self.reference_keypoint[1]) * scale_y
            radius_x = max(2.0, self._keypoint_focus_radius * scale_x)
            radius_y = max(2.0, self._keypoint_focus_radius * scale_y)
            offset_x = max(0, int(np.floor(keypoint_x - radius_x)))
            offset_y = max(0, int(np.floor(keypoint_y - radius_y)))
            x1 = min(template.shape[1], int(np.ceil(keypoint_x + radius_x)))
            y1 = min(template.shape[0], int(np.ceil(keypoint_y + radius_y)))
            edge_source = template[offset_y:y1, offset_x:x1]

        edges = self._edges(edge_source)

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
        pts += np.array([offset_x, offset_y])

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
            distance, rotated, best_x, best_y
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
                            distance, rotated, x, y
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

    def set_images(self, template, image):

        self.template = template
        self.image = image
        self.last_result = None
        return self

    def keypoint_ncc_seed(self, template=None, image=None,
                          radius=80.0, angle_step=1.0):
        """Find a global pose seed from a compact patch around the keypoint.

        This compares every pixel in the distinctive keypoint neighborhood with
        normalized correlation. Long
        repetitive template structures outside that neighborhood cannot dominate.
        """
        if template is None:
            template = self.template
        if image is None:
            image = self.image
        if self.reference_keypoint is None or radius <= 0:
            return None

        gray_template = self._to_gray(template)
        gray_image = self._to_gray(image)
        h, w = gray_template.shape
        keypoint_x = float(self.reference_keypoint[0])
        keypoint_y = float(self.reference_keypoint[1])
        radius = float(radius)
        x0 = max(0, int(np.floor(keypoint_x - radius)))
        x1 = min(w, int(np.ceil(keypoint_x + radius)))
        y0 = max(0, int(np.floor(keypoint_y - radius)))
        y1 = min(h, int(np.ceil(keypoint_y + radius)))
        patch = gray_template[y0:y1, x0:x1]
        if patch.shape[0] < 10 or patch.shape[1] < 10:
            raise ValueError("keypoint NCC patch is too small")
        if patch.shape[0] > gray_image.shape[0] or patch.shape[1] > gray_image.shape[1]:
            raise ValueError("keypoint NCC patch is larger than the search image")

        patch_center = ((patch.shape[1] - 1) / 2.0, (patch.shape[0] - 1) / 2.0)
        patch_keypoint = np.array([keypoint_x - x0, keypoint_y - y0], dtype=np.float64)
        # Full-frame normalized correlation dominates runtime on large images.
        # Search globally at a derived lower resolution, then confirm the winning
        # neighborhood at native resolution. The following chamfer stage still
        # performs the precise position refinement.
        search_scale = min(1.0, 1200.0 / max(gray_image.shape))
        if search_scale < 1.0:
            search_image = cv2.resize(
                gray_image, None, fx=search_scale, fy=search_scale,
                interpolation=cv2.INTER_AREA,
            )
        else:
            search_image = gray_image

        best = None
        coarse_candidates = []
        angles = self._inclusive_angle_range(
            self.coarse_angle_min,
            self.coarse_angle_max,
            float(angle_step),
        )
        for angle in angles:
            transform = cv2.getRotationMatrix2D(patch_center, -float(angle), 1.0)
            rotated_patch = cv2.warpAffine(
                patch, transform, (patch.shape[1], patch.shape[0]),
                flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE,
            )
            if search_scale < 1.0:
                search_patch = cv2.resize(
                    rotated_patch, None, fx=search_scale, fy=search_scale,
                    interpolation=cv2.INTER_AREA,
                )
            else:
                search_patch = rotated_patch
            correlation = cv2.matchTemplate(
                search_image, search_patch, cv2.TM_CCOEFF_NORMED
            )
            rotated_keypoint = transform[:, :2] @ patch_keypoint + transform[:, 2]
            keypoint_offset = np.array([
                keypoint_x - w / 2.0,
                keypoint_y - h / 2.0,
            ])
            rotated_offset = self.rotate_points(keypoint_offset[None, :], angle)[0]
            center_offset = (rotated_keypoint - rotated_offset) * search_scale
            # A small patch can correlate with image borders, but such a seed
            # would put the full reference center outside the image. Remove
            # those impossible candidates before selecting the NCC maximum.
            valid_x0 = max(0, int(np.ceil(-center_offset[0])))
            valid_y0 = max(0, int(np.ceil(-center_offset[1])))
            valid_x1 = min(correlation.shape[1], int(np.floor(search_image.shape[1] - center_offset[0])))
            valid_y1 = min(correlation.shape[0], int(np.floor(search_image.shape[0] - center_offset[1])))
            if valid_x0 >= valid_x1 or valid_y0 >= valid_y1:
                continue
            if valid_y0 > 0:
                correlation[:valid_y0, :] = -np.inf
            if valid_y1 < correlation.shape[0]:
                correlation[valid_y1:, :] = -np.inf
            if valid_x0 > 0:
                correlation[:, :valid_x0] = -np.inf
            if valid_x1 < correlation.shape[1]:
                correlation[:, valid_x1:] = -np.inf
            _minimum, maximum, _min_location, max_location = cv2.minMaxLoc(correlation)
            keypoint_abs = (
                np.array(max_location, dtype=np.float64) / search_scale
                + rotated_keypoint
            )
            template_center = keypoint_abs - rotated_offset
            candidate = (
                float(maximum), float(template_center[0]),
                float(template_center[1]), float(angle),
            )
            coarse_candidates.append(candidate)
            if best is None or maximum > best[0]:
                best = candidate
        if best is None or search_scale == 1.0:
            return best

        # Recheck the strongest coarse angles over the complete native-resolution
        # image. Keeping global position verification avoids choosing a different
        # repeated structure merely because it looked stronger after reduction.
        confirmed_best = None
        keypoint_offset = np.array([keypoint_x - w / 2.0, keypoint_y - h / 2.0])
        strongest_angles = sorted(coarse_candidates, reverse=True)[:7]
        for _coarse_score, _center_x, _center_y, angle in strongest_angles:
            transform = cv2.getRotationMatrix2D(patch_center, -angle, 1.0)
            rotated_patch = cv2.warpAffine(
                patch, transform, (patch.shape[1], patch.shape[0]),
                flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE,
            )
            rotated_keypoint = transform[:, :2] @ patch_keypoint + transform[:, 2]
            rotated_offset = self.rotate_points(keypoint_offset[None, :], angle)[0]
            correlation = cv2.matchTemplate(
                gray_image, rotated_patch, cv2.TM_CCOEFF_NORMED
            )
            center_offset = rotated_keypoint - rotated_offset
            valid_x0 = max(0, int(np.ceil(-center_offset[0])))
            valid_y0 = max(0, int(np.ceil(-center_offset[1])))
            valid_x1 = min(
                correlation.shape[1],
                int(np.floor(gray_image.shape[1] - center_offset[0])),
            )
            valid_y1 = min(
                correlation.shape[0],
                int(np.floor(gray_image.shape[0] - center_offset[1])),
            )
            if valid_x0 >= valid_x1 or valid_y0 >= valid_y1:
                continue
            correlation[:valid_y0, :] = -np.inf
            correlation[valid_y1:, :] = -np.inf
            correlation[:, :valid_x0] = -np.inf
            correlation[:, valid_x1:] = -np.inf
            _minimum, maximum, _min_location, max_location = cv2.minMaxLoc(correlation)
            keypoint_abs = (
                np.array(max_location, dtype=np.float64) + rotated_keypoint
            )
            template_center = keypoint_abs - rotated_offset
            candidate = (
                float(maximum), float(template_center[0]),
                float(template_center[1]), angle,
            )
            if confirmed_best is None or candidate[0] > confirmed_best[0]:
                confirmed_best = candidate
        return best if confirmed_best is None else confirmed_best

    @staticmethod
    def _orientation_representation(patch, mode):
        if mode == "intensity":
            return patch.astype(np.float32)
        if mode != "gradient":
            raise ValueError("orientation_mode must be 'gradient' or 'intensity'")
        gx = cv2.Sobel(patch, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(patch, cv2.CV_32F, 0, 1, ksize=3)
        return cv2.magnitude(gx, gy)

    def _orientation_context_angle(self, template, image,
                                   keypoint_x, keypoint_y,
                                   region, angle_step, refine_step, mode):
        """Estimate rotation from any reference-relative context rectangle."""
        gray_template = self._to_gray(template)
        gray_image = self._to_gray(image)
        reference_x = float(self.reference_keypoint[0])
        reference_y = float(self.reference_keypoint[1])
        if region is None:
            x0, y0 = 0, 0
            x1, y1 = gray_template.shape[1], gray_template.shape[0]
        else:
            if len(region) != 4:
                raise ValueError("orientation_region must be (x, y, width, height)")
            x, y, width, height = map(float, region)
            if width <= 0 or height <= 0:
                raise ValueError("orientation_region width and height must be positive")
            x0 = max(0, int(np.floor(x)))
            y0 = max(0, int(np.floor(y)))
            x1 = min(gray_template.shape[1], int(np.ceil(x + width)))
            y1 = min(gray_template.shape[0], int(np.ceil(y + height)))
        reference_patch = gray_template[y0:y1, x0:x1]
        if reference_patch.shape[0] < 20 or reference_patch.shape[1] < 10:
            raise ValueError("orientation_region is too small or outside the template")

        candidate_center = (
            float(keypoint_x) + (x0 + x1) / 2.0 - reference_x,
            float(keypoint_y) + (y0 + y1) / 2.0 - reference_y,
        )
        translation_tolerance = int(np.clip(
            round(min(reference_patch.shape[:2]) / 250.0), 2, 5
        ))
        candidate_patch = cv2.getRectSubPix(
            gray_image,
            (
                reference_patch.shape[1] + 2 * translation_tolerance,
                reference_patch.shape[0] + 2 * translation_tolerance,
            ),
            candidate_center,
        )
        rotation_center = (reference_x - x0, reference_y - y0)
        candidate_features = self._orientation_representation(candidate_patch, mode)
        def evaluate(angles, best=None):
            for angle in angles:
                transform = cv2.getRotationMatrix2D(
                    rotation_center, -float(angle), 1.0
                )
                rotated = cv2.warpAffine(
                    reference_patch, transform,
                    (reference_patch.shape[1], reference_patch.shape[0]),
                    flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE,
                )
                rotated_features = self._orientation_representation(rotated, mode)
                score = float(cv2.matchTemplate(
                    candidate_features, rotated_features, cv2.TM_CCOEFF_NORMED
                ).max())
                if best is None or score > best[0]:
                    best = (score, float(angle))
            return best

        best = evaluate(self._inclusive_angle_range(
            self.coarse_angle_min, self.coarse_angle_max, angle_step
        ))
        if best is not None and 0 < refine_step < angle_step:
            intermediate_step = max(refine_step, angle_step / 10.0)
            refine_min = max(self.coarse_angle_min, best[1] - angle_step)
            refine_max = min(self.coarse_angle_max, best[1] + angle_step)
            best = evaluate(self._inclusive_angle_range(
                refine_min, refine_max, intermediate_step
            ), best)
            if refine_step < intermediate_step:
                refine_min = max(self.coarse_angle_min, best[1] - intermediate_step)
                refine_max = min(self.coarse_angle_max, best[1] + intermediate_step)
                best = evaluate(self._inclusive_angle_range(
                    refine_min, refine_max, refine_step
                ), best)
        return None if best is None else best[1]

    def _apply_context_angle(self, result, template, image,
                             region, angle_step, refine_step, mode):
        if self.reference_keypoint is None:
            return result
        angle = self._orientation_context_angle(
            template, image, result["x_abs"], result["y_abs"],
            region, angle_step, refine_step, mode,
        )
        if angle is None:
            return result
        updated = dict(result)
        updated["angle"] = angle
        th, tw = template.shape[:2]
        offset = np.array([
            float(self.reference_keypoint[0]) - tw / 2.0,
            float(self.reference_keypoint[1]) - th / 2.0,
        ])
        rotated_offset = self.rotate_points(offset[None, :], angle)[0]
        updated["template_center_x_abs"] = float(result["x_abs"] - rotated_offset[0])
        updated["template_center_y_abs"] = float(result["y_abs"] - rotated_offset[1])
        return updated

    def match_feature(self, template=None, image=None,
                      position_radius=80.0,
                      position_angle_step=1.0,
                      chamfer_focus_radius=None,
                      refine_xy_window=8.0,
                      orientation_region=None,
                      orientation_angle_step=0.1,
                      orientation_refine_step=0.01,
                      orientation_mode="gradient"):
        """Match any annotated reference feature without an image pose prior.

        A compact patch around the reference keypoint finds position globally.
        An independent, arbitrary reference-relative context rectangle estimates
        orientation. Focused chamfer performs the final local position refinement.
        ``orientation_region`` is ``(x, y, width, height)`` in template pixels;
        ``None`` uses the full reference image. Orientation is searched globally
        at ``orientation_angle_step`` and locally at ``orientation_refine_step``.
        """
        if template is None:
            template = self.template
        if image is None:
            image = self.image
        if template is None or image is None:
            raise ValueError("No images set")
        if self.reference_keypoint is None:
            raise ValueError("match_feature requires reference_keypoint")

        self.template = template
        self.image = image
        old_focus_radius = self._keypoint_focus_radius
        try:
            focus_radius = (
                float(position_radius) if chamfer_focus_radius is None
                else float(chamfer_focus_radius)
            )
            self._keypoint_focus_radius = focus_radius
            seed = self.keypoint_ncc_seed(
                template, image, radius=position_radius,
                angle_step=position_angle_step,
            )
            if seed is None:
                raise RuntimeError("Could not find a keypoint NCC seed")
            _correlation, center_x, center_y, angle = seed
            result = self._match_with_initial_pose(
                center_x, center_y, angle, float(refine_xy_window),
                template=template, image=image,
            )
            result = self._apply_context_angle(
                result, template, image, orientation_region,
                float(orientation_angle_step), float(orientation_refine_step),
                orientation_mode,
            )
            self.last_result = result
            return result
        finally:
            self._keypoint_focus_radius = old_focus_radius

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

        img_pyr = self.create_pyramid(image)
        tmp_pyr = self.create_pyramid(template)
        pose = None
        score = None

        for level in range(self.pyramid_levels):
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
                    window=max(1.0, xy_window / scale),
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
                    window=max(5.0, xy_window / max(scale, 1)),
                )

                x, y, a = pose
                angles = self._fine_angles(a)
                pose, score = self.search_level(
                    distance,
                    template_pts,
                    angles,
                    xy_step=1,
                    center=(x, y),
                    window=10,
                )

        pose, score = self.refine_pose_subpixel(
            distance,
            template_pts,
            pose,
        )

        result = self._result_from_pose(pose, score, template, image)
        self.last_result = result

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
            "image_size": (int(iw), int(ih)),
        }

    def draw_result_on_canvas(self,
                              canvas,
                              result=None,
                              template=None,
                              thickness=2,
                              border_color=(0, 165, 255),
                              draw_border=False,
                              alpha=None,
                              **_unused_draw_options):
        """Blend the matched reference patch onto a copy of the canvas."""

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

        if alpha is None:
            alpha = 0.35
        alpha = float(np.clip(alpha, 0.0, 1.0))
        patch_pixels = warped_mask > 0
        canvas_pixels = canvas[patch_pixels].astype(np.float32)
        reference_pixels = warped_reference[patch_pixels].astype(np.float32)
        canvas[patch_pixels] = np.clip(
            canvas_pixels * (1.0 - alpha) + reference_pixels * alpha,
            0, 255,
        ).astype(np.uint8)

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

class CoarseFineChamferMatcher:
    """Adaptive public matcher with a deliberately small configuration surface.

    Search mechanics are derived from the reference size and requested angular
    accuracy. The low-level engine remains private so vision-function YAML files
    do not need to expose pyramid, sampling, or refinement implementation details.

    Refinement pipeline
    -------------------
    1. Derive internal settings
       The reference dimensions determine the number of pyramid levels, the
       keypoint-neighborhood radius, the local XY window, the edge-point budget,
       and the ignored reference border. ``angle_accuracy_deg`` determines the
       final orientation step; the class derives all coarser angle steps from it.

    2. Global position seed
       A square grayscale patch around ``reference_keypoint`` is rotated across
       the allowed angle range. Normalized cross-correlation searches a derived
       lower-resolution copy of large input images, and the winning neighborhood
       is confirmed at native resolution. This supplies an unconstrained global
       position and approximate rotation without input-image pose metadata.

    3. Focused coarse-to-fine chamfer position
       Edge extraction is performed on the reference neighborhood before its
       gradient threshold is calculated. This prevents large repetitive edges
       elsewhere in the reference from suppressing the distinctive local feature.
       At the coarsest pyramid level, chamfer distance searches only the derived
       window around the correlation seed. Each following level doubles the pose
       coordinates and searches a smaller grid: first with two-pixel XY spacing,
       then with one-pixel spacing and a narrower angle range.

    4. Subpixel chamfer refinement
       The best full-resolution pose is refined in three progressively smaller
       neighborhoods. The passes use decreasing XY and angular radii and evaluate
       bilinearly interpolated edge-distance values, producing a subpixel keypoint.
       The reported chamfer score is the mean reference-edge distance normalized
       by the image diagonal; lower values are better.

    5. Independent orientation refinement
       Position and orientation are intentionally separated. With the keypoint
       fixed, the full reference gradient context is compared at every derived
       coarse orientation. A small automatically derived translation tolerance
       absorbs residual subpixel-position error. The neighborhood around the best
       angle is rescanned twice: first at one tenth of the coarse step and then at
       ``angle_accuracy_deg``. Finally, the template center is recomputed for the
       refined angle while the reported keypoint coordinate remains unchanged.

    The default keypoint is the reference center. Supplying an annotated keypoint
    is recommended when a particular physical feature must be reported.
    """

    def __init__(self):
        self.template = None
        self.image = None
        self.reference_keypoint = None
        self.last_result = None
        self.derived_settings = {}
        self._engine = None

    @staticmethod
    def _derive_settings(template, max_rotation_deg, angle_accuracy_deg):
        height, width = template.shape[:2]
        minimum_size = float(min(height, width))
        accuracy = float(angle_accuracy_deg)
        rotation = abs(float(max_rotation_deg))
        if accuracy <= 0:
            raise ValueError("angle_accuracy_deg must be greater than zero")
        if rotation > 180:
            raise ValueError("max_rotation_deg must be between 0 and 180")

        # Global position already comes from dense NCC, so the chamfer stage is
        # only a local refinement. More than two levels adds quantization without
        # improving capture range; small references stay at native resolution.
        pyramid_levels = 2 if minimum_size >= 256 else 1

        orientation_coarse_step = 1.0
        position_angle_step = min(
            5.0,
            max(1.0, min(1.0, max(0.1, accuracy * 10.0)) * 5.0),
        )
        feature_radius = float(np.clip(round(minimum_size * 0.125), 48, 160))
        refine_xy_window = float(np.clip(round(feature_radius * 0.10), 6, 16))
        max_template_points = int(np.clip(round(np.sqrt(height * width) * 2.3), 800, 2500))
        ignore_border = int(np.clip(round(minimum_size / 160.0), 2, 8))

        return {
            "pyramid_levels": pyramid_levels,
            "edge_percentile": 98.0,
            "max_template_points": max_template_points,
            "ignore_border": ignore_border,
            "feature_radius": feature_radius,
            "refine_xy_window": refine_xy_window,
            "position_angle_step": position_angle_step,
            "orientation_coarse_step": orientation_coarse_step,
            "orientation_refine_step": accuracy,
            "max_rotation_deg": rotation,
        }

    def set_images(self, template, image, reference_keypoint=None):
        self.template = template
        self.image = image
        self.reference_keypoint = reference_keypoint
        self.last_result = None
        return self

    def match(self, template=None, image=None, reference_keypoint=None,
              max_rotation_deg=10.0, angle_accuracy_deg=0.01):
        """Find and refine the reference pose in ``image``.

        Args:
            template: Reference image. Uses the image passed to ``set_images``
                when omitted.
            image: Search image. Uses the image passed to ``set_images`` when
                omitted.
            reference_keypoint: ``(x, y)`` feature in reference pixels. Uses the
                value passed to ``set_images`` or the reference center.
            max_rotation_deg: Symmetric rotation range searched around zero.
            angle_accuracy_deg: Final local orientation search step. The global
                and intermediate steps are derived automatically.

        Returns:
            Dictionary containing the subpixel keypoint (``x_abs``, ``y_abs``),
            refined ``angle``, normalized chamfer ``score``, and reference-center
            information used for drawing the transformed reference.

        Note:
            ``angle_accuracy_deg`` is numerical search resolution, not guaranteed
            physical accuracy. Camera calibration, optical distortion, image
            noise, and feature symmetry still limit measurement accuracy.
        """
        if template is None:
            template = self.template
        if image is None:
            image = self.image
        if template is None or image is None:
            raise ValueError("No images set")

        if reference_keypoint is None:
            reference_keypoint = self.reference_keypoint
        if reference_keypoint is None:
            reference_keypoint = (template.shape[1] / 2.0, template.shape[0] / 2.0)
        reference_keypoint = tuple(map(float, reference_keypoint))

        settings = self._derive_settings(
            template, max_rotation_deg, angle_accuracy_deg
        )
        engine = _ChamferSearchEngine(
            pyramid_levels=settings["pyramid_levels"],
            edge_percentile=settings["edge_percentile"],
            max_template_points=settings["max_template_points"],
            ignore_border=settings["ignore_border"],
            reference_keypoint=reference_keypoint,
            coarse_angle_min=-settings["max_rotation_deg"],
            coarse_angle_max=settings["max_rotation_deg"],
            coarse_angle_step=settings["position_angle_step"],
            refine_angle_window=min(
                settings["max_rotation_deg"],
                max(1.0, settings["position_angle_step"] * 5.0),
            ),
            refine_angle_step=max(0.25, settings["position_angle_step"] / 2.0),
            fine_angle_window=max(0.4, settings["orientation_coarse_step"] * 4.0),
            fine_angle_step=max(0.05, settings["orientation_coarse_step"] / 2.0),
        )
        engine.set_images(template, image)
        result = engine.match_feature(
            position_radius=settings["feature_radius"],
            position_angle_step=settings["position_angle_step"],
            chamfer_focus_radius=settings["feature_radius"],
            refine_xy_window=settings["refine_xy_window"],
            orientation_region=None,
            orientation_angle_step=settings["orientation_coarse_step"],
            orientation_refine_step=settings["orientation_refine_step"],
            orientation_mode="gradient",
        )

        self.template = template
        self.image = image
        self.reference_keypoint = reference_keypoint
        self._engine = engine
        self.derived_settings = settings
        self.last_result = result
        return result

    def draw_result_on_canvas(self, canvas, result=None, template=None,
                              alpha=0.35, **kwargs):
        if self._engine is None:
            raise ValueError("No match available")
        return self._engine.draw_result_on_canvas(
            canvas, result=result or self.last_result,
            template=template if template is not None else self.template,
            alpha=alpha, **kwargs,
        )

    def draw_reference_lines_on_canvas(self, canvas, result=None, template=None,
                                       **kwargs):
        if self._engine is None:
            raise ValueError("No match available")
        return self._engine.draw_reference_lines_on_canvas(
            canvas, result=result or self.last_result,
            template=template if template is not None else self.template,
            **kwargs,
        )


def _reference_paths(process_file_path):
    if process_file_path in (None, ""):
        raise PictureReferenceMatcherError(
            "Process file path is not set; cannot locate matcher reference image."
        )
    process_path = Path(process_file_path)
    base = process_path.with_suffix("")
    image_path = base.parent / f"{base.name}_matcher_reference_image.png"
    metadata_path = base.parent / f"{base.name}_matcher_reference_image_metadata.json"
    if not image_path.is_file():
        raise PictureReferenceMatcherError(f"Reference image not found: {image_path}")
    return image_path, metadata_path


def _reference_keypoint(metadata_path, reference):
    """Read the static reference annotation, never an input-image pose prior."""
    if metadata_path.is_file():
        try:
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
            point = data.get("reference_keypoint_px", {})
            return float(point["x"]), float(point["y"])
        except (OSError, ValueError, KeyError, TypeError):
            pass
    return reference.shape[1] / 2.0, reference.shape[0] / 2.0


def picture_reference_matcher(
        image_processing_handler: "ImageProcessingHandler",
        max_rotation_deg=10.0,
        angle_accuracy_deg=0.01,
        max_score_threshold=0.002,
        draw_reference=True,
        draw_lines=True,
        logger=None):
    """Run the adaptive matcher using pm_vision_manager conventions."""
    reference_path, metadata_path = _reference_paths(
        image_processing_handler.process_file_path
    )
    reference = cv2.imread(str(reference_path), cv2.IMREAD_COLOR)
    if reference is None:
        raise PictureReferenceMatcherError(
            f"Could not read reference image: {reference_path}"
        )
    image = image_processing_handler.get_processing_image()
    keypoint = _reference_keypoint(metadata_path, reference)

    matcher = CoarseFineChamferMatcher().set_images(
        reference, image, reference_keypoint=keypoint,
    )
    if logger:
        logger.info("PictureReferenceMatcher assessment started.")
    assessment_start = perf_counter()
    try:
        result = matcher.match(
            max_rotation_deg=float(max_rotation_deg),
            angle_accuracy_deg=float(angle_accuracy_deg),
        )
    except Exception:
        assessment_duration = perf_counter() - assessment_start
        if logger:
            logger.error(
                "PictureReferenceMatcher assessment failed after "
                f"{assessment_duration:.3f} s."
            )
        raise
    assessment_duration = perf_counter() - assessment_start
    if logger:
        logger.info(
            "PictureReferenceMatcher assessment finished in "
            f"{assessment_duration:.3f} s."
        )

    x = float(result["x_abs"])
    y = float(result["y_abs"])
    x_camera, y_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x, y)
    point = image_processing_handler.new_vision_point_result()
    point.axis_value_1 = x_camera
    point.axis_value_2 = y_camera
    point.axis_suffix_1 = image_processing_handler.camera_axis_1
    point.axis_suffix_2 = image_processing_handler.camera_axis_2
    point.angle = float(result["angle"])
    image_processing_handler.append_vision_obj_to_results(point)

    score = float(result["score"])
    maximum = float(max_score_threshold)
    medium = maximum * 0.25
    quality = "failed" if score > maximum else "medium" if score > medium else "good"
    image_processing_handler.set_quality_scores(
        "PictureReferenceMatcher",
        {
            "score": score,
            "medium_score_threshold": medium,
            "max_score_threshold": maximum,
            "fit_quality": quality,
            "lower_score_is_better": True,
        },
    )

    derived = matcher.derived_settings
    image_processing_handler.append_vision_process_debug(
        "PictureReferenceMatcher: "
        f"reference='{reference_path.name}', x={x:.2f}px, y={y:.2f}px, "
        f"angle={result['angle']:.3f}deg, score={score:.6f}, "
        f"pyramid_levels={derived['pyramid_levels']}, "
        f"feature_radius={derived['feature_radius']:.0f}px"
    )

    if quality != "good":
        message = (
            f"PictureReferenceMatcher {quality} fit: score={score:.6f}, "
            f"maximum={maximum:.6f}"
        )
        if logger:
            logger.warning(message)
        image_processing_handler.append_vision_process_debug(message)

    if draw_reference or draw_lines:
        canvas = image_processing_handler.get_visual_elements_canvas()
        if draw_reference:
            image_bgr = image
            if image_bgr.ndim == 2:
                image_bgr = cv2.cvtColor(image_bgr, cv2.COLOR_GRAY2BGR)
            reference_overlay = matcher.draw_result_on_canvas(
                image_bgr, alpha=0.35
            )
            changed_pixels = np.any(reference_overlay != image_bgr, axis=2)
            canvas[changed_pixels] = reference_overlay[changed_pixels]
        if draw_lines:
            canvas = matcher.draw_reference_lines_on_canvas(
                canvas, thickness=2
            )
        image_processing_handler.apply_visual_elements_canvas(canvas)

    image_processing_handler.set_vision_ok(quality != "failed")
    return result
