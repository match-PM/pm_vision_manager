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
                    mode:str, 
                    draw_circles: bool,
                    logger = None):
    
    if not image_processing_handler.is_process_image_binary():
        raise ImageNotBinaryError()
  
    frame_processed = image_processing_handler.get_processing_image()

    canvas = image_processing_handler.get_visual_elements_canvas()

    # Do a contour detection
    contours, _ = cv2.findContours(frame_processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
    
    for index, contour in enumerate(contours):
        point_coordinates = []

        if index > 100:
            if logger:
                logger.warn("More than 100 contours found. Only the first 100 will be processed")
                image_processing_handler.append_vision_process_debug("More than 100 contours found. Only the first 100 will be processed")
            break

        for point in contour:
            x, y = point[0]  # Extract x, y from the contour point
            point_coordinates.append([x, y])
        
        if len(point_coordinates) < 4:
            if logger:
                logger.debug("Contour has less than 3 points")
            continue
        
        if mode == 'taubinSVD':
            x, y, r, s = circle_fit.taubinSVD(point_coordinates)
        elif mode == 'hyperSVD':
            x, y, r, s = circle_fit.hyperSVD(point_coordinates)
        elif mode == 'prattSVD':
            x, y, r, s = circle_fit.prattSVD(point_coordinates)
        elif mode == 'lm':
            x, y, r, s = circle_fit.lm(point_coordinates)
        elif mode == 'riemannSWFLa':
            x, y, r, s = circle_fit.riemannSWFLa(point_coordinates)
        elif mode == 'kmh':
            x, y, r, s = circle_fit.kmh(point_coordinates)
        elif mode == 'hyperLSQ':
            x, y, r, s = circle_fit.hyperLSQ(point_coordinates)
        else:
            x, y, r, s = circle_fit.standardLSQ(point_coordinates)

        radius_um = r * image_processing_handler.umPROpixel

        if radius_um < max_radius and radius_um > min_radius:
            found_circles_x.append(x)
            found_circles_y.append(y)
            found_circles_r.append(r)
            found_circles_r_um.append(radius_um)
            found_circles_s.append(s)
        else:
            if logger:
                logger.debug(f"Circle with radius {radius_um} out of range {min_radius} - {max_radius}")

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
    
    if draw_circles:
        
        line_size = image_processing_handler.img_height // 200 + 1
        #logger.warn(f"Line size: {line_size}")
        #x_tl,y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(int(round(x_tl_roi)),int(round(y_tl_roi)))
        # Draw the circumference of the circle.
        for ind in range(len(found_circles_x)):
            x_tl_roi = found_circles_x[ind]
            y_tl_roi = found_circles_y[ind]
            radius = found_circles_r[ind]
            cv2.circle(canvas, (int(x_tl_roi), int(y_tl_roi)), int(round(radius)), (0, 255, 0), line_size)
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(canvas, (int(x_tl_roi), int(y_tl_roi)), 1, (0, 0, 255), line_size)

        image_processing_handler.apply_visual_elements_canvas(canvas)
