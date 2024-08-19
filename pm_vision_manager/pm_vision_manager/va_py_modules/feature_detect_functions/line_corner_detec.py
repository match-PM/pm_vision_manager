# Import the necessary libraries
import cv2 # OpenCV library
import numpy as np
import os
from math import pi                              
from pm_vision_manager.va_py_modules.vision_utils import rotate_image
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler, ImageNotBinaryError, ImageNotGrayScaleError

def fitLine_pre(image_processing_handler: ImageProcessingHandler, line_selection: str, search_accuracy: str, minLineLength:int, logger = None):
  if not image_processing_handler.is_process_image_binary():
    raise ImageNotBinaryError()
  
  frame_processed = image_processing_handler.get_processing_image()

  frame_processed = cv2.Canny(frame_processed, 10, 200, 3)
  minLineLength_pix = int(image_processing_handler.pixelPROum*minLineLength)

  threshold_adaptive = int(minLineLength * 0.3)
  maxLineGap_adaptive = int(minLineLength * 2.5)
  
  match search_accuracy:
    case "coarse":
      rho_adaptive = 1
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
      # theta_adaptive = int(60800*rho_adaptive)

  lines = cv2.HoughLinesP(frame_processed,rho = rho_adaptive,theta = np.pi/theta_adaptive, threshold = threshold_adaptive, minLineLength = minLineLength_pix, maxLineGap = maxLineGap_adaptive)
  # threshold - how many points can repsent a line
  canvas = image_processing_handler.get_visual_elements_canvas()  
  # Draw detected lines on the original image

  if lines is not None:

    # calculate delas of x1 and x2
    deltas_x = [abs(line[0][2] - line[0][0]) for line in lines]
    deltas_y = [abs(line[0][3] - line[0][1]) for line in lines]

    logger.debug(f"{(deltas_x)} are the deltas x!")
    logger.debug(f"{(deltas_y)} are the deltas y!")

    delta_deltas = [delta_x - delta_y for delta_x, delta_y in zip(deltas_x, deltas_y)]

    logger.debug(f"{(delta_deltas)} are the delta deltas!")
                 
    # vector of inidies of lines that are vertical or horizontal
    horizontal_lines_indicies = [idx for idx, value in enumerate(delta_deltas) if value >= 0]
    vertical_lines_indicies = [idx for idx, value in enumerate(delta_deltas) if value < 0]

    if logger:
      logger.info(f"{(horizontal_lines_indicies)} are horizontal lines!")
      logger.info(f"{(vertical_lines_indicies)} are vertical lines!")

    # calculate midpoints of horizontal lines
    midpoints_horizontal = [((line[0][0] + line[0][2]) / 2, (line[0][1] + line[0][3]) / 2) for idx, line in enumerate(lines) if idx in horizontal_lines_indicies]
    
    # calculate midpoints of vertical lines
    midpoints_vertical = [((line[0][0] + line[0][2]) / 2, (line[0][1] + line[0][3]) / 2) for idx, line in enumerate(lines) if idx in vertical_lines_indicies]

    if logger:
      logger.debug(f"{(midpoints_horizontal)} are horizontal midpoints!")
      logger.debug(f"{(midpoints_vertical)} are vertical midpoints!")

    # calculate max differnece between x values in vertical midpoints
    left_vert_mid_ind = []
    right_vert_mid_ind = []
    if midpoints_vertical:
      max_x_mid_vert = max(point[0] for point in midpoints_vertical)
      min_x_mid_vert = min(point[0] for point in midpoints_vertical)
      abs_x_mid_vert = abs(max_x_mid_vert + min_x_mid_vert)/2

      if logger:
        logger.debug(f"{(max_x_mid_vert)} is max x mid vert!")
        logger.debug(f"{(min_x_mid_vert)} is min x mid vert!")
        logger.debug(f"{(abs_x_mid_vert)} is abs x mid vert!")

      left_vert_mid_points = [point for ind, point in enumerate(midpoints_vertical) if point[0] <= abs_x_mid_vert]
      right_vert_mid_points = [point for ind, point in enumerate(midpoints_vertical) if point[0] > abs_x_mid_vert]

      left_vert_mid_ind = [ind for ind, point in enumerate(midpoints_vertical) if point[0] <= abs_x_mid_vert]
      right_vert_mid_ind = [ind for ind, point in enumerate(midpoints_vertical) if point[0] > abs_x_mid_vert]

    # max_y_mid_vert = max(point[1] for point in midpoints_vertical)
    # min_y_mid_vert = min(point[1] for point in midpoints_vertical)
    # abs_y_mid_vert = abs(max_y_mid_vert - min_y_mid_vert)/2


    # max_x_mid_hor = max(point[0] for point in midpoints_horizontal)
    # min_x_mid_hor = min(point[0] for point in midpoints_horizontal)
    # abs_x_mid_hor = abs(max_x_mid_hor - min_x_mid_hor)/2

    top_hor_mid_ind = []
    bottom_hor_mid_ind = []
    if midpoints_horizontal:
      max_y_mid_hor = max(point[1] for point in midpoints_horizontal)
      min_y_mid_hor = min(point[1] for point in midpoints_horizontal)
      abs_y_mid_hor = abs(max_y_mid_hor + min_y_mid_hor)/2

      if logger:
        logger.debug(f"{(max_y_mid_hor)} is max y mid hor!")
        logger.debug(f"{(min_y_mid_hor)} is min y mid hor!")
        logger.debug(f"{(abs_y_mid_hor)} is abs y mid hor!")

      top_hor_mid_points = [point for point in midpoints_horizontal if point[1] <= abs_y_mid_hor]
      bottom_hor_mid_points = [point for point in midpoints_horizontal if point[1] > abs_y_mid_hor]

      top_hor_mid_ind = [ind for ind, point in enumerate(midpoints_horizontal) if point[1] <= abs_y_mid_hor]
      bottom_hor_mid_ind = [ind for ind, point in enumerate(midpoints_horizontal) if point[1] > abs_y_mid_hor]

    selected_line = None

    logger.error(f"{(line_selection)} is the line selection!")

    match line_selection:
      case "left":
        if left_vert_mid_ind:
          line_ind_left_vertical = vertical_lines_indicies[left_vert_mid_ind[0]]
          selected_line = lines[line_ind_left_vertical]
          logger.error("Found line according to 'left' selection")
          logger.error(f"Found {len(left_vert_mid_ind)} left vertical lines!")
      case "right":
        logger.error("right")
        if right_vert_mid_ind:
          line_ind_right_vertical = vertical_lines_indicies[right_vert_mid_ind[0]]
          selected_line = lines[line_ind_right_vertical]
          logger.error("Found line according to 'right' selection")
          logger.error(f"Found {len(right_vert_mid_ind)} right vertical lines!")

      case "top":
        if top_hor_mid_ind:
          line_ind_top_horizontal = horizontal_lines_indicies[top_hor_mid_ind[0]]
          selected_line = lines[line_ind_top_horizontal]
          logger.error("Found line according to 'top' selection")
          logger.error(f"Found {len(top_hor_mid_ind)} top horizontal lines!")

      case "bottom":
        if bottom_hor_mid_ind:
          line_ind_bottom_horizontal = horizontal_lines_indicies[bottom_hor_mid_ind[0]]
          selected_line = lines[line_ind_bottom_horizontal]
          logger.error("Found line according to 'bottom' selection")
          logger.error(f"Found {len(bottom_hor_mid_ind)} bottom horizontal lines!")

    if selected_line is not None:
      logger.error("Drawing selected line")
      x1, y1, x2, y2 = selected_line[0]
      return selected_line
    
    else:
      if logger:
        logger.error("No lines detected")
      return None

  else:
    if logger:
      logger.error("No lines detected")
    return None

def fitLine(image_processing_handler: ImageProcessingHandler, line_selection: str, search_accuracy: str, minLineLength:int, logger = None):
  
  line = fitLine_pre(image_processing_handler, line_selection, search_accuracy, minLineLength, logger)
  
  if line is None:
    image_processing_handler.set_vision_ok(False)
    return
  
  # threshold - how many points can repsent a line
  canvas = image_processing_handler.get_visual_elements_canvas()  

  x1, y1, x2, y2 = line[0]

  cv2.line(canvas,(x1,y1),(x2,y2),(0,255,0),2)

  x1_cs_camera, y1_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x1,y1)
  x2_cs_camera, y2_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x2,y2)

  line_length_um = np.sqrt((x2_cs_camera - x1_cs_camera)**2 + (y2_cs_camera - y1_cs_camera)**2)

  if x2_cs_camera - x1_cs_camera == 0:
    line_angle = 0
  else:
    line_angle = np.arctan((y2_cs_camera - y1_cs_camera)/(x2_cs_camera - x1_cs_camera)) * 180/pi

  line = image_processing_handler.new_vision_line_result()
  line.point_1.axis_value_1 = x1_cs_camera
  line.point_1.axis_value_2 = y1_cs_camera
  line.point_1.axis_suffix_1 = image_processing_handler.camera_axis_1
  line.point_1.axis_suffix_2 = image_processing_handler.camera_axis_2
  line.point_2.axis_value_1 = x2_cs_camera
  line.point_2.axis_value_2 = y2_cs_camera
  line.point_2.axis_suffix_1 = image_processing_handler.camera_axis_1
  line.point_2.axis_suffix_2 = image_processing_handler.camera_axis_2
  line.point_mid.axis_suffix_1 = image_processing_handler.camera_axis_1
  line.point_mid.axis_suffix_2 = image_processing_handler.camera_axis_2
  line.point_mid.axis_value_1 = (x1_cs_camera + x2_cs_camera) / 2
  line.point_mid.axis_value_2 = (y1_cs_camera + y2_cs_camera) / 2
  line.length = line_length_um
  line.angle = float(line_angle)

  #image_processing_handler.set_processing_image(frame_processed)
  image_processing_handler.apply_visual_elements_canvas(canvas)
  image_processing_handler.append_vision_obj_to_results(line)

def cornerDetection(image_processing_handler: ImageProcessingHandler, 
                    line_1_selection: str, 
                    line_2_selection: str, 
                    search_accuracy: str, 
                    minLineLength_1:float,
                    minLineLength_2:float,
                    logger = None):
  
  if not image_processing_handler.is_process_image_binary():
    raise ImageNotBinaryError()
  
  if line_1_selection == line_2_selection:
    if logger:
      logger.error("Line 1 and Line 2 cannot be the same!")
    image_processing_handler.set_vision_ok(False)
    return
  
  line_1 = fitLine_pre(image_processing_handler, line_1_selection, search_accuracy, minLineLength_1, logger)
  
  if line_1 is None:
    if logger:
      logger.error("No line for input 1 detected")
    image_processing_handler.set_vision_ok(False)
    return
  
  # threshold - how many points can repsent a line
  canvas = image_processing_handler.get_visual_elements_canvas()  

  line_1_x1, line_1_y1, line_1_x2, line_1_y2 = line_1[0]

  cv2.line(canvas,(line_1_x1,line_1_y1),(line_1_x2,line_1_y2),(0,255,0),2)


  line_2 = fitLine_pre(image_processing_handler, line_2_selection, search_accuracy, minLineLength_2, logger)

  if line_2 is None:
    if logger:
      logger.error("No line for input 2 detected")
    image_processing_handler.set_vision_ok(False)
    return
  
  line_2_x1, line_2_y1, line_2_x2, line_2_y2 = line_2[0]

  cv2.line(canvas,(line_2_x1,line_2_y1),(line_2_x2,line_2_y2),(0,255,0),2)

  result = calculate_intersection(line_1, line_2,logger)

  if result is None:
    if logger:
      logger.error("No intersection point detected!")
    image_processing_handler.set_vision_ok(False)
    return
  
  x = result[0]
  y = result[1]

  # check if x,y out of bounds
  if x < 0 or x > image_processing_handler.get_processing_image().shape[1] or y < 0 or y > image_processing_handler.get_processing_image().shape[0]:
    if logger:
      logger.error("No valid point of intersection found!")
    image_processing_handler.apply_visual_elements_canvas(canvas)
    image_processing_handler.set_vision_ok(False)
    return
  
  logger.error(f"Intersection point: {x}, {y}")
  cv2.drawMarker(canvas, (int(x), int(y)), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=50, thickness=2)
  
  x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x,y)
  point = image_processing_handler.new_vision_point_result()
  point.axis_value_1 = x_cs_camera
  point.axis_value_2 = y_cs_camera
  point.axis_suffix_1 = image_processing_handler.camera_axis_1
  point.axis_suffix_2 = image_processing_handler.camera_axis_2
  image_processing_handler.append_vision_obj_to_results(point)
  image_processing_handler.apply_visual_elements_canvas(canvas)
  image_processing_handler.set_vision_ok(True)


# def calculate_intersection(line1, line2,logger=None):
#     # Extract coordinates of the lines
#     (x1, y1, x2, y2), (x3, y3, x4, y4) = line1[0], line2[0]
#     logger.error(f"Line 1: {x1}, {y1}, {x2}, {y2}")
#     logger.error(f"Line 2: {x3}, {y3}, {x4}, {y4}")
#     # Calculate slopes (m)
#     m1 = (y2 - y1) / (x2 - x1)
#     m2 = (y4 - y3) / (x4 - x3)

#     if x2 == x1:


#     # Calculate y-intercepts (c)
#     c1 = y1 - m1 * x1
#     c2 = y3 - m2 * x3

#     # Calculate intersection point
#     if m1 == m2:
#         return None  # Lines are parallel
#     else:
#         x = (c2 - c1) / (m1 - m2)
#         y = m1 * x + c1
#         return (x, y)

def calculate_intersection(line1, line2,logger):
    # Extract coordinates of the lines
    (x1, y1, x2, y2), (x3, y3, x4, y4) = line1[0], line2[0]

    # Calculate slopes (m)
    if x1 == x2:
        m1 = None  # Line 1 is vertical
    else:
        m1 = (y2 - y1) / (x2 - x1)

    if x3 == x4:
        m2 = None  # Line 2 is vertical
    else:
        m2 = (y4 - y3) / (x4 - x3)

    # Calculate y-intercepts (c)
    if m1 is not None:
        c1 = y1 - m1 * x1
    else:
        c1 = None

    if m2 is not None:
        c2 = y3 - m2 * x3
    else:
        c2 = None

    # Calculate intersection point
    if m1 == m2:
        if m1 is None:
            # Both lines are vertical, no intersection point
            return None
        else:
            # Lines are parallel and non-vertical
            return None
    elif m1 is None:
        # Line 1 is vertical
        x = x1
        y = m2 * x + c2
        return x, y
    elif m2 is None:
        # Line 2 is vertical
        x = x3
        y = m1 * x + c1
        return x, y
    else:
        # General case
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1
        return x, y
