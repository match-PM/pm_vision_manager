# Import the necessary libraries
from rclpy.node import Node # Handles the creation of nodes
import cv2 # OpenCV library
import numpy as np
import os
from math import pi                              
from pm_vision_manager.va_py_modules.vision_utils import rotate_image
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler, ImageNotBinaryError, ImageNotGrayScaleError
from pm_vision_manager.va_py_modules.feature_detect_functions.line_corner_detec import fitLine, cornerDetection
import time

def threshold(image_processing_handler: ImageProcessingHandler, thresh: int, maxval:int, type:str) -> None:
  frame_processed = image_processing_handler.get_processing_image()
  _Command = "cv2." + type
  _,frame_processed = cv2.threshold(frame_processed,thresh,maxval,exec(_Command))
  image_processing_handler.set_processing_image(frame_processed)

def adaptiveThreshold(image_processing_handler: ImageProcessingHandler, maxValue, adaptiveMethod, thresholdType, blockSize, cValue):
  _Command_adaptiveMethod = "cv2." + adaptiveMethod
  _Command_thresholdType = "cv2." + thresholdType
  frame_processed  = image_processing_handler.get_processing_image()
  frame_processed = cv2.adaptiveThreshold(frame_processed, maxValue, exec(_Command_adaptiveMethod), exec(_Command_thresholdType), blockSize, cValue)
  image_processing_handler.set_processing_image(frame_processed)

def bitwise_not(image_processing_handler: ImageProcessingHandler):
  frame_processed = image_processing_handler.get_processing_image()
  frame_processed = cv2.bitwise_not(frame_processed)
  image_processing_handler.set_processing_image(frame_processed)

def bgr2gray(image_processing_handler: ImageProcessingHandler):
  frame_processed = image_processing_handler.get_processing_image()
  if len(frame_processed.shape)==3:
    frame_processed = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2GRAY)
    image_processing_handler.set_processing_image(frame_processed)

def roi(image_processing_handler: ImageProcessingHandler, ROI_center_x_c: float, ROI_center_y_c:float, ROI_height:float, ROI_width:float):

  ROI_center_x_i, ROI_center_y_i = image_processing_handler.CS_Camera_TO_Image(ROI_center_x_c, ROI_center_y_c)
  ROI_center_x_pix, ROI_center_y_pix = image_processing_handler.CS_Image_TO_Pixel(ROI_center_x_i, ROI_center_y_i)
  ROI_half_height_pix = int(round(image_processing_handler.pixelPROum*ROI_height/2))
  ROI_half_width_pix = int(round(image_processing_handler.pixelPROum*ROI_width/2))
  ROI_top_left_x_pix = ROI_center_x_pix - ROI_half_width_pix
  ROI_bottom_right_x_pix = ROI_center_x_pix + ROI_half_width_pix
  ROI_top_left_y_pix = ROI_center_y_pix + ROI_half_height_pix
  ROI_bottom_right_y_pix = ROI_center_y_pix - ROI_half_height_pix

  frame_processed = image_processing_handler.get_processing_image()

  ROI_CS_CV_top_left_x, ROI_CS_CV_top_left_y = image_processing_handler.CS_Conv_Pixel_Center_TO_Top_Left(frame_processed.shape[1], frame_processed.shape[0], ROI_top_left_x_pix, ROI_top_left_y_pix)
  ROI_CS_CV_bottom_right_x, ROI_CS_CV_bottom_right_y = image_processing_handler.CS_Conv_Pixel_Center_TO_Top_Left(frame_processed.shape[1], frame_processed.shape[0], ROI_bottom_right_x_pix, ROI_bottom_right_y_pix)
  
  if (ROI_CS_CV_top_left_x>0 and 
    ROI_CS_CV_top_left_y>0 and 
    ROI_CS_CV_bottom_right_x <= image_processing_handler.img_width and 
    ROI_CS_CV_bottom_right_y <= image_processing_handler.img_height):
    _frame_processed = frame_processed[ROI_CS_CV_top_left_y:ROI_CS_CV_bottom_right_y, ROI_CS_CV_top_left_x:ROI_CS_CV_bottom_right_x]
    image_processing_handler.set_roi_settings(ROI_CS_CV_top_left_x, ROI_CS_CV_top_left_y, ROI_CS_CV_bottom_right_x, ROI_CS_CV_bottom_right_y)

    image_processing_handler.frame_visual_elements = cv2.rectangle(image_processing_handler.frame_visual_elements,(ROI_CS_CV_top_left_x,ROI_CS_CV_top_left_y),(ROI_CS_CV_bottom_right_x,ROI_CS_CV_bottom_right_y),(240,32,160),3)
    
    image_processing_handler.set_processing_image(_frame_processed)

  else:
    image_processing_handler.set_vision_ok(False)

def canny(image_processing_handler: ImageProcessingHandler, threshold1, threshold2, aperatureSize, L2gradient:str,logger = None):
  frame_processed = image_processing_handler.get_processing_image()
  frame_processed = cv2.Canny(frame_processed, threshold1, threshold2, aperatureSize)
  image_processing_handler.set_processing_image(frame_processed)


def findContours(image_processing_handler: ImageProcessingHandler, draw_contours:bool, mode:str, method:str, fill:bool):
  if not image_processing_handler.is_process_image_grayscale():
    raise ImageNotGrayScaleError()
  _Command_mode = "cv2." + mode
  _Command_method = "cv2." + method
  #contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), exec(_Command_method))  # Keine Ahnung warum das nicht funktioniert!!!
  frame_processed = image_processing_handler.get_processing_image()
  contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), cv2.CHAIN_APPROX_SIMPLE)
  if fill:
    cv2.fillPoly(frame_processed,pts=contours,color=(255,255,255))
      
  if draw_contours:
    canvas = image_processing_handler.get_visual_elements_canvas()
    cv2.drawContours(canvas, contours, -1, (0,255,75), 2)
    image_processing_handler.apply_visual_elements_canvas(canvas)

  image_processing_handler.set_processing_image(frame_processed)

def minEnclosingCircle(image_processing_handler: ImageProcessingHandler,draw_circles:bool, mode:str, method:str):
  if not image_processing_handler.is_process_image_grayscale():
    raise ImageNotGrayScaleError()
  
  frame_processed = image_processing_handler.get_processing_image()
  contours,hierarchy = cv2.findContours(frame_processed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  print("Number of contours detected:", len(contours))
  # select the first contour
  cnt = contours[0]
  (x_tl_roi, y_tl_roi),radius = cv2.minEnclosingCircle(cnt)
  x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(int(round(x_tl_roi)),int(round(y_tl_roi)))
  radius_um=radius*image_processing_handler.umPROpixel
  if radius <= 0.5: # this is in pixel
    image_processing_handler.set_vision_ok(False)
    return 

  circle_result_dict={"Circle":{
    'axis_1': x_cs_camera,
    'axis_2': y_cs_camera,
    'axis_1_suffix': image_processing_handler.camera_axis_1,
    'axis_2_suffix': image_processing_handler.camera_axis_2,
    "radius":radius_um,
    "Unit": "um"
    }}
  
  if draw_circles:
    canvas = image_processing_handler.get_visual_elements_canvas()
    #x_tl,y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(int(round(x_tl_roi)),int(round(y_tl_roi)))
    # Draw the circumference of the circle.
    cv2.circle(canvas, (int(x_tl_roi), int(y_tl_roi)), int(round(radius)), (0, 255, 0), 2)
    # Draw a small circle (of radius 1) to show the center.
    cv2.circle(canvas, (int(x_tl_roi), int(y_tl_roi)), 1, (0, 0, 255), 2)
    image_processing_handler.apply_visual_elements_canvas(canvas)

  image_processing_handler.append_to_results(circle_result_dict)
  image_processing_handler.set_processing_image(frame_processed)

def houghLinesP(image_processing_handler: ImageProcessingHandler, threshold, minLineLength,maxLineGap):    
  if not image_processing_handler.is_process_image_grayscale():
    raise ImageNotGrayScaleError()
  frame_processed = image_processing_handler.get_processing_image()
  lines = cv2.HoughLinesP(frame_processed,rho = 1,theta = 1*np.pi/180,threshold = threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)
  canvas = image_processing_handler.get_visual_elements_canvas()
  HoughLinesP_results_list=[]
  if lines is not None:
    for x1,y1,x2,y2 in lines[0]:
      x1,y1 = image_processing_handler.CS_Conv_ROI_Pix_TO_Img_Pix(x1,y1)
      x2,y2 = image_processing_handler.CS_Conv_ROI_Pix_TO_Img_Pix(x2,y2)
      cv2.line(canvas,(x1,y1),(x2,y2),(0,255,0),2)

      x1_cs_camera, y1_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x1,y1)
      x2_cs_camera, y2_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x2,y2)

      line = image_processing_handler.new_vision_line_result()
      line.point_1.axis_value_1 = x1_cs_camera
      line.point_1.axis_value_2 = y1_cs_camera
      line.point_1.axis_suffix_1 = image_processing_handler.camera_axis_1
      line.point_1.axis_suffix_2 = image_processing_handler.camera_axis_2
      line.point_2.axis_value_1 = x2_cs_camera
      line.point_2.axis_value_2 = y2_cs_camera
      line.point_2.axis_suffix_1 = image_processing_handler.camera_axis_1
      line.point_2.axis_suffix_2 = image_processing_handler.camera_axis_2
      image_processing_handler.append_vision_obj_to_results(line)

      HoughLinesP_results_list.append({
        'Point_1': {'axis_1': x1_cs_camera,"axis_2":y2_cs_camera},
        'Point_2': {'axis_1': x2_cs_camera,"axis_2":y2_cs_camera},
        'axis_1_suffix': image_processing_handler.camera_axis_1,
        'axis_2_suffix': image_processing_handler.camera_axis_2,
        'angle': "to be added",
        'length': "to be added",
        "Unit": "um",
        "angle_unit": "degree"
        })
      
    image_processing_handler.apply_visual_elements_canvas(canvas)
    HoughLinesP_results_dict={"Lines": HoughLinesP_results_list}
    image_processing_handler.append_to_results(HoughLinesP_results_dict)
                  
  else:
    image_processing_handler.set_vision_ok(False)


def selectArea(image_processing_handler: ImageProcessingHandler, mode:str, method: str, max_area, min_area):
  frame_processed = image_processing_handler.get_processing_image()
  _Command_mode = "cv2." + mode
  _Command_method = "cv2." + method
  #contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), exec(_Command_method))  # Keine Ahnung warum das nicht funktioniert!!!
  contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), cv2.CHAIN_APPROX_SIMPLE)
  all_areas= []
  for cnt in contours:
    area= cv2.contourArea(cnt)
    all_areas.append(area)
  contour_frame = np.zeros((frame_processed.shape[0], frame_processed.shape[1]), dtype = np.uint8)
  area_found = False
  for index, area_item in enumerate(all_areas):
        
    if area_item<max_area and area_item>min_area:
      frame_processed = cv2.drawContours(contour_frame, contours, index, color=(255,255,255), thickness=cv2.FILLED)
      area_found = True
                      
  if not area_found:
    image_processing_handler.set_vision_ok(False)
    frame_processed = np.zeros((frame_processed.shape[0], frame_processed.shape[1]), dtype = np.uint8)
  else:
    image_processing_handler.set_vision_ok(True)
  image_processing_handler.set_processing_image(frame_processed)  
  
def morphologyExOpening(image_processing_handler: ImageProcessingHandler,kernelsize:int):
  if not image_processing_handler.is_process_image_binary():
    raise ImageNotBinaryError()
  frame_processed = image_processing_handler.get_processing_image()
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
  frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_OPEN, kernel)
  image_processing_handler.set_processing_image(frame_processed)

def morphologyExClosing(image_processing_handler: ImageProcessingHandler,kernelsize:int):
  if not image_processing_handler.is_process_image_binary():
    raise ImageNotBinaryError()
  frame_processed = image_processing_handler.get_processing_image()
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
  frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_CLOSE, kernel)
  image_processing_handler.set_processing_image(frame_processed)


def horizontal(image_processing_handler: ImageProcessingHandler, h_kernelsize):
  frame_processed = image_processing_handler.get_processing_image()
  horizontal_size = image_processing_handler.get_initial_image().shape[1] // h_kernelsize
  horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
  frame_processed = cv2.erode(frame_processed, horizontalStructure)
  frame_processed = cv2.dilate(frame_processed, horizontalStructure)
  image_processing_handler.set_processing_image(frame_processed)

def vertical(image_processing_handler: ImageProcessingHandler, v_kernelsize):
  frame_processed = image_processing_handler.get_processing_image()
  vertical_size = image_processing_handler.get_initial_image().shape[0] // v_kernelsize
  verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
  frame_processed = cv2.erode(frame_processed, verticalStructure)
  frame_processed = cv2.dilate(frame_processed, verticalStructure)
  image_processing_handler.set_processing_image(frame_processed)


def blur(image_processing_handler: ImageProcessingHandler, kernelsize: int, blur_type: str, gaus_std: int):

  frame_processed = image_processing_handler.get_processing_image()
  if blur_type == "GaussianBlur":
    frame_processed = cv2.GaussianBlur(frame_processed, (kernelsize, kernelsize), gaus_std)
  elif blur_type == "Blur":
    frame_processed = cv2.blur(frame_processed, (kernelsize, kernelsize))
  elif blur_type == "medianBlur":
    frame_processed = cv2.medianBlur(frame_processed, kernelsize)
  else:
    image_processing_handler.set_vision_ok(False)

  image_processing_handler.set_processing_image(frame_processed)

def morphologyExGradient(image_processing_handler: ImageProcessingHandler, kernelsize:int):
  frame_processed = image_processing_handler.get_processing_image()
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
  frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_GRADIENT, kernel)
  image_processing_handler.set_processing_image(frame_processed)

def Errosion(image_processing_handler: ImageProcessingHandler, kernelsize:int, iterations:int):
  frame_processed = image_processing_handler.get_processing_image()
  kernel = np.ones((kernelsize, kernelsize), np.uint8)
  frame_processed = cv2.erode(frame_processed, kernel, iterations=iterations)
  image_processing_handler.set_processing_image(frame_processed)

def Dilation(image_processing_handler: ImageProcessingHandler, kernelsize:int, iterations:int):
  frame_processed = image_processing_handler.get_processing_image()
  kernel = np.ones((kernelsize, kernelsize), np.uint8)
  frame_processed = cv2.dilate(frame_processed, kernel, iterations=iterations)
  image_processing_handler.set_processing_image(frame_processed)

def HoughCircles(image_processing_handler: ImageProcessingHandler,
                 draw_circles:bool,
                 method:str,
                 dp: float,
                 minDist,
                 param1,
                 param2,
                 minRadius,
                 maxRadius):

  if not image_processing_handler.is_process_image_grayscale():
    raise ImageNotGrayScaleError()
  
  frame_processed = image_processing_handler.get_processing_image()

  _Command_method = "cv2." + method
  detected_circles = cv2.HoughCircles(frame_processed,cv2.HOUGH_GRADIENT, dp, minDist, param1 = param1, param2 = param2, minRadius = minRadius, maxRadius = maxRadius)
  
  if detected_circles is not None:
    print("Cirlces Detected")
    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
    HoughCircles_reslults_list=[]
    for pt in detected_circles[0, :]:
      x, y, r = pt[0], pt[1], pt[2]

      x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x,y)
      radius_um=r*image_processing_handler.umPROpixel
      #print(str(image_processing_handler.camera_axis_1)+'-Coordinate:'+ str(x_cs_camera))
      #print(str(image_processing_handler.camera_axis_2)+'-Coordinate:'+ str(y_cs_camera))
      #print('Radius: '+ str(radius_um))
      circle = image_processing_handler.new_vision_circle_result()
      circle.radius = radius_um
      circle.center_point.axis_value_1 = x_cs_camera
      circle.center_point.axis_value_2 = y_cs_camera
      circle.center_point.axis_suffix_1 = image_processing_handler.camera_axis_1
      circle.center_point.axis_suffix_2 = image_processing_handler.camera_axis_2

      image_processing_handler.append_vision_obj_to_results(circle)

      # HoughCircles_reslults_list.append({
      #   'axis_1': x_cs_camera,
      #   'axis_2': y_cs_camera,
      #   'axis_1_suffix': image_processing_handler.camera_axis_1,
      #   'axis_2_suffix': image_processing_handler.camera_axis_2,
      #   "radius":radius_um,
      #   "Unit": "um"
      #   })

      if draw_circles:
        canvas = image_processing_handler.get_visual_elements_canvas()
        #x_tl,y_tl = image_processing_handler.CS_Conv_ROI_Pix_TO_Img_Pix(x,y)
        # Draw the circumference of the circle.
        cv2.circle(canvas, (x, y), r, (0, 255, 0), 2)
        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(canvas, (x, y), 1, (0, 0, 255), 2)
        image_processing_handler.apply_visual_elements_canvas(canvas)

    #HouchCircles_results_dict={"Circles": HoughCircles_reslults_list}
    #image_processing_handler.append_to_results(HouchCircles_results_dict)
  else:
    image_processing_handler.set_vision_ok(False)


def drawCS(image_processing_handler: ImageProcessingHandler):
  CS_frame = np.zeros((image_processing_handler.get_initial_image().shape[0]+image_processing_handler.get_initial_image().shape[1], 
                       image_processing_handler.get_initial_image().shape[0]+image_processing_handler.get_initial_image().shape[1], 
                       3), 
                       dtype = np.uint8)
  if image_processing_handler.camera_axis_1 == 'z' or image_processing_handler.camera_axis_1 == 'Z':
    color_axis_1 = (255, 0, 0)
  elif image_processing_handler.camera_axis_1 == 'y' or image_processing_handler.camera_axis_1 == 'Y':
    color_axis_1 = (0, 255, 0)
  else:
    color_axis_1 = (0, 0, 255)

  if image_processing_handler.camera_axis_2 == 'z' or image_processing_handler.camera_axis_2 == 'Z':
    color_axis_2 = (255, 0, 0)
  elif image_processing_handler.camera_axis_2 == 'x' or image_processing_handler.camera_axis_2 == 'X':
    color_axis_2 = (0, 0, 255)
  else:
    color_axis_2 = (0, 255, 0)

  #draw axis_1
  cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(CS_frame.shape[1], int(CS_frame.shape[0]/2)), color_axis_1, 2, 1)
  #draw axis_2
  if image_processing_handler.camera_axis_2_angle == '+':
    cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(int(CS_frame.shape[1]/2), 0), color_axis_2, 2, 1)
  else:
    cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(int(CS_frame.shape[1]/2), CS_frame.shape[0]), color_axis_2 , 2, 1)
  CS_frame= rotate_image(CS_frame,image_processing_handler.camera_axis_1_angle)
  center = CS_frame.shape
  x = center[1]/2 - image_processing_handler.img_width/2
  y = center[0]/2 - image_processing_handler.img_height/2
  crop_img = CS_frame[int(y):int(y+image_processing_handler.img_height), int(x):int(x+image_processing_handler.img_width)]

  image_processing_handler.frame_visual_elements = image_processing_handler.create_vision_element_overlay(image_processing_handler.frame_visual_elements,crop_img)

def drawGrid(image_processing_handler: ImageProcessingHandler, grid_spacing):

  Grid_frame = np.zeros((image_processing_handler.get_initial_image().shape[0]+image_processing_handler.get_initial_image().shape[1], 
                         image_processing_handler.get_initial_image().shape[0]+image_processing_handler.get_initial_image().shape[1], 3), 
                         dtype = np.uint8)
  #numb = int(round((Grid_frame.shape[0]/2)/grid_spacing*self.pixelPROum))+1 # This is a bug
  numb = int(round((image_processing_handler.fov_width/2)/grid_spacing))+1

  cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2), 0),(int(Grid_frame.shape[1]/2), Grid_frame.shape[1]), (255, 0, 0), 1, 1)
  cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)), (255, 0, 0), 1, 1)
  
  for n in range(numb):
    #Draw horizontal lines
    pixel_delta=int(n*grid_spacing*image_processing_handler.pixelPROum)
    cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)+pixel_delta),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)+pixel_delta), (255, 0, 0), 1, 1)
    cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)-pixel_delta),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)-pixel_delta), (255, 0, 0), 1, 1)
    # draw vertical lines
    cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2)+pixel_delta, 0),(int(Grid_frame.shape[1]/2)+pixel_delta, Grid_frame.shape[1]), (255, 0, 0), 1, 1)
    cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2)-pixel_delta, 0),(int(Grid_frame.shape[1]/2)-pixel_delta, Grid_frame.shape[1]), (255, 0, 0), 1, 1)
    
  Grid_frame= rotate_image(Grid_frame,image_processing_handler.camera_axis_1_angle)
  center = Grid_frame.shape
  x = center[1]/2 - image_processing_handler.img_width/2
  y = center[0]/2 - image_processing_handler.img_height/2

  crop_img = Grid_frame[int(y):int(y+image_processing_handler.img_height), int(x):int(x+image_processing_handler.img_width)]
  image_processing_handler.frame_visual_elements = image_processing_handler.create_vision_element_overlay(image_processing_handler.frame_visual_elements,crop_img)
  cv2.putText(img=image_processing_handler.frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)

def saveImage(image_processing_handler: ImageProcessingHandler, 
              prefix: str, with_vision_elements: bool, save_in_cross_val :bool, logger = None):
  
  if not os.path.exists(image_processing_handler.process_db_path):
    os.makedirs(image_processing_handler.process_db_path)
  
  # image_processing_handler.image_name comes from (image_name = f"{self.vision_process_id}_{image_in_folder}")
  # in "vision_assistant_class.py" line 250. Maybe good to know... --> Don't use "/" in your process_uid
  image_name=f"{image_processing_handler.process_db_path}/{image_processing_handler.current_image_name}{prefix}.png"

  #if not os.path.isfile(image_name) and (not image_processing_handler.cross_val_running or save_in_cross_val):
  if (not image_processing_handler.cross_val_running or save_in_cross_val):
    if with_vision_elements:
      image_to_save = image_processing_handler.create_vision_element_overlay(image_processing_handler.get_display_image(),
                                                                             image_processing_handler.frame_visual_elements)
      
    else:
      image_to_save = image_processing_handler.get_processing_image()

    cv2.imwrite(image_name, image_to_save)
    Save_image_results_dict={"Image saved:": image_name} # image_processing_handler.
    image_processing_handler.append_to_results(Save_image_results_dict)



def reduce_saturation(image_processing_handler: ImageProcessingHandler, 
                      HueMin: int, HueMax: int, f_reduce_s: int):
  """
  Converts the BGR-image into the HSV-Colorspace to reduce the saturation for the hues given
  in the 'HueRange'. Then the methods returns an BGR-image.
    
  :param bgr_img: Image in BGR.
  :param HueMin: Min value for the range of hue values, which saturation will be reduced.
  :param HueMax: Max value for the range of hue values, which saturation will be reduced.
  :param f_reduce_s: Factor of how much the saturation should be reduced.
  :return: Image in BGR.
  """
  # TODO Evtl. wäre ein Test gut, zuschauen ob das Bild ein BGR-Image ist

  frame_processed = image_processing_handler.get_processing_image()

  hsv_img = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2HSV)  # Convert given BGR-image into the HSV-ColorSpace
  h, s, v = cv2.split(hsv_img)    # Splits image into its three channels
  # Reduces saturation by factor x in a given range of the hue-values
  s = np.where((h >= HueMin) & (h <= HueMax), (s / f_reduce_s).astype('uint8'), s)  
  new_hsv_img = cv2.merge([h, s, v])  # Gets all three channels back together
  frame_processed = cv2.cvtColor(new_hsv_img, cv2.COLOR_HSV2BGR) # Converts image back into BGR-Colorspace

  image_processing_handler.set_processing_image(frame_processed)


def CLAHE_on_V_Channel(image_processing_handler: ImageProcessingHandler,
                       clipLimit: float, tileGridSize_M: int, tileGridSize_N: int):
  """
  Apply the Contrast Limited Adaptive Histogram Equalization (CLAHE) the Value-Channel of the converted HSV-Image.
  Helps to get a better contrast of the brightness in the image. Therefore it should get more easy to find edges for example.

  :param bgr_img: Image in BGR.
  :param clipLimit: This is the threshold for contrast limiting
  :param tileGridSize: Divides the input image into M x N tiles and 
                       then applies histogram equalization to each local tile
  :return: Image in BGR.
  """
  # TODO Evtl. wäre ein Test gut, zuschauen ob das Bild ein BGR-Image ist

  frame_processed = image_processing_handler.get_processing_image()

  clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize_M,tileGridSize_N)) # Create CLAHE-Object
  hsv_img = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2HSV)  # Convert given BGR-image into the HSV-ColorSpace
  h, s, v = cv2.split(hsv_img)    # Splits image into its three channels
  v = clahe.apply(v)  # Apply contrasting vie CLAHE on the value channel of the HSV-image
  v = (v).astype('uint8') # Important for merging to image
  new_hsv_img = cv2.merge([h, s, v])  # Gets all three channels back together
  frame_processed = cv2.cvtColor(new_hsv_img, cv2.COLOR_HSV2BGR) # Converts image back into BGR-Colorspace

  image_processing_handler.set_processing_image(frame_processed)


def EqualizeHist(image_processing_handler: ImageProcessingHandler):
  """
  Equalizes the Histogram of an Gray-Image or a Channel of an Image.
  """
  frame_processed = image_processing_handler.get_processing_image()
  frame_processed = cv2.equalizeHist(frame_processed)
  image_processing_handler.set_processing_image(frame_processed)


def example_function(image_processing_handler: ImageProcessingHandler):
  """
  This is an example function for the process image function.
  """
  # Check if image is binary if thats necessary for your function
  if not image_processing_handler.is_process_image_binary():
    raise ImageNotBinaryError()
  
  # Check if image is grayscale if thats necessary for your function
  if not image_processing_handler.is_process_image_grayscale():
    raise ImageNotGrayScaleError()  

  # get copy of the current processing frame
  frame_processed = image_processing_handler.get_processing_image()

  # if you want to draw something on the display frame, get a canvas 
  canvas = image_processing_handler.get_visual_elements_canvas()

  #Example coordinates in canvas cs (top left)
  x = 1
  y = 1
  # Convert the example coordinates to camera cs
  x_cs_camera, y_cs_camera = image_processing_handler.CS_CV_TO_camera_with_ROI(x,y)
  # create example results dict
  example_results ={
        'axis_1': x_cs_camera,
        'axis_2': y_cs_camera,
        'axis_1_suffix': image_processing_handler.camera_axis_1,  # axis_naming is defined in camera config
        'axis_2_suffix': image_processing_handler.camera_axis_2,  # axis_naming is defined in camera config
        "Unit": "um"}
  # Create a key for the results
  example_results_dict={"Example_Results_Key(e.a. Point)": example_results}
  # append to results list
  image_processing_handler.append_to_results(example_results_dict)
  
  # One you have drawn on the canvas, you can apply it to the display frame
  image_processing_handler.apply_visual_elements_canvas(canvas)

  # Set the processing image once you have modified it
  image_processing_handler.set_processing_image(frame_processed)


#################################################################################################################

def process_image(vision_node: Node, image_processing_handler: ImageProcessingHandler, pipeline_dict_list:list):
  image_processing_handler.init_begin()
  try:
    for list_item in pipeline_dict_list:

      #Break the for loop early if vision is not okay.
      if not image_processing_handler.get_vision_ok():
        # Break the for loop
        break

      for key, function_parameter in list_item.items():
        match key:
          case "Set_Camera_Exposure_Time":
            active = function_parameter['active']
            value = function_parameter['value']
            if active and not image_processing_handler.cross_val_running:
              image_processing_handler.set_camera_exposure_time(value)  
              image_processing_handler.stop_image_subscription = False    
              # Break the for loop
              break
          
          case "SetCoAxLightBool":
            active = function_parameter['active']
            set_state = function_parameter['set_state']
            #if active and not image_processing_handler.cross_val_running:
            if active:
              image_processing_handler.set_camera_coax_light_bool(set_state)
              image_processing_handler.stop_image_subscription = False
              # Break the for loop
              break
          
          case "SetCoAxLight":
            active = function_parameter['active']
            value = function_parameter['value']
            #if active and not image_processing_handler.cross_val_running:
            if active:
              image_processing_handler.set_camera_coax_light(value)  
              image_processing_handler.stop_image_subscription = False
              # Break the for loop
              break

          case "SetRingLight":
            active = function_parameter['active']

            bool_list = [function_parameter['enable_Q1'],
                         function_parameter['enable_Q2'],
                         function_parameter['enable_Q3'],
                         function_parameter['enable_Q4']]

            rgb_list =  [function_parameter['r_value'],
                         function_parameter['g_value'],
                         function_parameter['b_value']] 
                  
            #if active and not image_processing_handler.cross_val_running:
            if active:
              image_processing_handler.set_ring_light(bool_list, rgb_list)  
              image_processing_handler.stop_image_subscription = False
              # Break the for loop
              break


          case "Threshold":
            active = function_parameter['active']
            p_thresh = function_parameter['thresh']
            p_maxval = function_parameter['maxval']
            p_type = function_parameter['type'] 
            if active:
              threshold(image_processing_handler = image_processing_handler,
                        thresh = p_thresh,
                        maxval = p_maxval,
                        type = p_type)

          case "AdaptiveThreshold":
            active = function_parameter['active']
            p_maxValue = function_parameter['maxValue']
            p_adaptiveMethod = function_parameter['adaptiveMethod']
            p_thresholdType = function_parameter['thresholdType']
            p_blockSize = function_parameter['blockSize'] 
            p_C_Value = function_parameter['C']
            if active:
              adaptiveThreshold(image_processing_handler = image_processing_handler,
                                maxValue=p_maxValue,
                                adaptiveMethod=p_adaptiveMethod,
                                thresholdType = p_thresholdType,
                                blockSize= p_blockSize,
                                cValue=p_C_Value)
              
          case "Bitwise_Not":
              active = function_parameter['active']
              if active:
                bitwise_not(image_processing_handler=image_processing_handler)
                  
          case "BGR2GRAY":
              active = function_parameter['active']
              if active:
                bgr2gray(image_processing_handler=image_processing_handler)

          case "ROI":
              active = function_parameter['active']
              if active:
                if not image_processing_handler.roi_used:
                  p_ROI_center_x_c = function_parameter['ROI_center_x']
                  p_ROI_center_y_c = function_parameter['ROI_center_y']
                  p_ROI_height = function_parameter['ROI_height']
                  p_ROI_width = function_parameter['ROI_width']    
                  roi(image_processing_handler=image_processing_handler,
                      ROI_center_x_c=p_ROI_center_x_c,
                      ROI_center_y_c=p_ROI_center_y_c,
                      ROI_height=p_ROI_height,
                      ROI_width=p_ROI_width)
                else:
                  vision_node.get_logger().warning('ROI already used! ROI can only be applied once!')  
                  pass

          case "Canny":
            active = function_parameter['active']
            p_threshold1 = function_parameter['threshold1']
            p_threshold2 = function_parameter['threshold2']
            p_aperatureSize = function_parameter['aperatureSize']
            p_L2gradient = function_parameter['L2gradient'] 

            if active:
                canny(image_processing_handler=image_processing_handler,
                      threshold1=p_threshold1,
                      threshold2=p_threshold2,
                      aperatureSize=p_aperatureSize,
                      L2gradient=p_L2gradient,
                      logger = vision_node.get_logger())
                
          case "FindContours":
            active = function_parameter['active']
            p_draw_contours = function_parameter['draw_contours']
            p_mode = function_parameter['mode']
            p_method = function_parameter['method']
            p_fill = function_parameter['fill']

            if active:
              findContours(image_processing_handler=image_processing_handler,
                            draw_contours=p_draw_contours,
                            mode=p_mode,
                            method=p_method,
                            fill=p_fill)

          case "MinEnclosingCircle":
            active = function_parameter['active']
            p_draw_circles = function_parameter['draw_circles']
            p_mode = function_parameter['mode']
            p_method = function_parameter['method']
            if active:
              minEnclosingCircle(image_processing_handler=image_processing_handler,
                                  draw_circles=p_draw_circles,
                                  mode=p_mode,
                                  method=p_method)   
                    
          case "HoughLinesP":
            active = function_parameter['active']
            p_threshold = function_parameter['threshold']
            p_minLineLength = function_parameter['minLineLength']
            p_maxLineGap = function_parameter['maxLineGap']              
            if active:
              houghLinesP(image_processing_handler=image_processing_handler,
                          threshold=p_threshold,
                          minLineLength=p_minLineLength,
                          maxLineGap=p_maxLineGap)

          case "Select_Area":
            active = function_parameter['active']
            p_mode = function_parameter['mode']
            p_method = function_parameter['method']
            p_max_area = function_parameter['max_area']
            p_min_area = function_parameter['min_area']
            if active:
              selectArea(image_processing_handler=image_processing_handler,
                          mode=p_mode,
                          method=p_method,
                          max_area=p_max_area,
                          min_area=p_min_area)

          case "Morphology_Ex_Opening":
            active = function_parameter['active']
            p_kernelsize = function_parameter['kernelsize']

            if active:
              morphologyExOpening(image_processing_handler=image_processing_handler,
                                  kernelsize=p_kernelsize)
                                  
          case "Morphology_Ex_Closing":
            active = function_parameter['active']
            p_kernelsize = function_parameter['kernelsize']

            if active:
              morphologyExClosing(image_processing_handler=image_processing_handler,
                                  kernelsize=p_kernelsize)
          
          case "Horizontal":
            active = function_parameter['active']
            p_h_kernelsize = function_parameter['h_kernelsize']

            if active:
              horizontal(image_processing_handler=image_processing_handler,
                         h_kernelsize=p_h_kernelsize)             
              
          case "Vertical":
            active = function_parameter['active']
            p_v_kernelsize = function_parameter['v_kernelsize']

            if active:
              vertical(image_processing_handler=image_processing_handler,
                        v_kernelsize=p_v_kernelsize)  
              
          case "Blur":
            active = function_parameter.get('active')
            p_kernelsize = function_parameter.get('kernelsize')
            p_blur_type = function_parameter.get('type')
            p_gaus_std = function_parameter.get('gaus_std')

            if active:
              blur(image_processing_handler=image_processing_handler,
                   kernelsize=p_kernelsize, blur_type=p_blur_type, gaus_std=p_gaus_std)             

          case "Morphology_Ex_Gradient":
            active = function_parameter['active']
            p_kernelsize = function_parameter['kernelsize']

            if active:
              morphologyExGradient(image_processing_handler=image_processing_handler,
                                   kernelsize=p_kernelsize)

          case "Errosion":
            active = function_parameter['active']
            p_kernelsize = function_parameter['kernelsize']
            p_iterations = function_parameter['iterations']

            if active:
              Errosion(image_processing_handler=image_processing_handler,
                       kernelsize=p_kernelsize,
                       iterations=p_iterations)

          case "Dilation":
            active = function_parameter['active']
            p_kernelsize = function_parameter['kernelsize']
            p_iterations = function_parameter['iterations']

            if active:
              Dilation(image_processing_handler=image_processing_handler,
                       kernelsize=p_kernelsize,
                       iterations=p_iterations)

          case "Save_Image":
            active = function_parameter['active']
            p_prefix = function_parameter['prefix']
            p_with_vision_elements = function_parameter['with_vision_elements']
            p_save_in_cross_val = function_parameter['save_in_cross_val']
            if active:
              saveImage(image_processing_handler=image_processing_handler,
                        prefix = p_prefix,
                        with_vision_elements = p_with_vision_elements,
                        save_in_cross_val = p_save_in_cross_val,
                        logger = vision_node.get_logger())
                                
          case "Draw_Grid":
            active = function_parameter['active']
            p_grid_spacing = function_parameter['grid_spacing']
            
            if p_grid_spacing == 0:
              break

            if active:
              drawGrid(image_processing_handler=image_processing_handler,
                       grid_spacing=p_grid_spacing)

          case "Draw_CS":
            active = function_parameter['active']
            if active:
              drawCS(image_processing_handler=image_processing_handler)

          case "HoughCircles":
            active = function_parameter['active']
            p_draw_circles = function_parameter['draw_circles']
            p_method = function_parameter['method']
            p_dp = function_parameter['dp']
            p_minDist = function_parameter['minDist']
            p_param1 = function_parameter['param1']
            p_param2 = function_parameter['param2']
            p_minRadius = int(round(function_parameter['minRadius']* image_processing_handler.pixelPROum)) # conv in Pixel
            p_maxRadius = int(round(function_parameter['maxRadius']* image_processing_handler.pixelPROum)) # conv in Pixel
            if active:
              HoughCircles(image_processing_handler=image_processing_handler,
                                          draw_circles=p_draw_circles,
                                          method=p_method,
                                          dp=p_dp,
                                          minDist=p_minDist,
                                          param1=p_param1,
                                          param2=p_param2,
                                          minRadius=p_minRadius,
                                          maxRadius=p_maxRadius)
              
          case "ReduceSaturation":
            active = function_parameter.get('active')
            p_HueMin = function_parameter.get('HueMin')
            p_HueMax = function_parameter.get('HueMax')
            p_f_reduce_s = function_parameter.get('f_reduce_s')
            if active:
              reduce_saturation(
                image_processing_handler=image_processing_handler,
                HueMin=p_HueMin,
                HueMax=p_HueMax,
                f_reduce_s=p_f_reduce_s
              )

          case "CLAHE_on_V_Channel":
            active = function_parameter.get('active')
            p_clipLimit = function_parameter.get('clipLimit')
            p_tileGridSize_M = function_parameter.get('tileGridSize_M')
            p_tileGridSize_N = function_parameter.get('tileGridSize_N')
            if active:
              CLAHE_on_V_Channel(
                image_processing_handler=image_processing_handler,
                clipLimit=p_clipLimit,
                tileGridSize_M=p_tileGridSize_M,
                tileGridSize_N=p_tileGridSize_N
              )

          case "EqualizeHist":
            active = function_parameter.get('active')
            if active:
              EqualizeHist(image_processing_handler=image_processing_handler)

          case "FitLine":
            active = function_parameter.get('active')
            p_line_selection = function_parameter.get('line selection')
            p_search_accuracy= function_parameter.get('search accuracy')
            p_minLineLength = function_parameter.get('minLineLength')
            #p_threshold = function_parameter.get('threshold')
            #p_minLineLength = function_parameter.get('minLineLength')
            #p_maxLineGap = function_parameter.get('maxLineGap')
            if active:
              fitLine(image_processing_handler=image_processing_handler, line_selection=p_line_selection, search_accuracy=p_search_accuracy, minLineLength=p_minLineLength, logger = vision_node.get_logger())
              #fitLine(image_processing_handler,p_rho,p_theta,p_threshold,p_minLineLength, p_maxLineGap, logger = vision_node.get_logger())              

          case "CornerDetection":
            active = function_parameter.get('active')
            p_line_1_selection = function_parameter.get('line_1_selection')
            p_line_2_selection = function_parameter.get('line_2_selection')
            p_search_accuracy= function_parameter.get('search_accuracy')
            p_minLineLength_1 = function_parameter.get('minLineLength_1')
            p_minLineLength_2 = function_parameter.get('minLineLength_2')

            if active:
              cornerDetection(image_processing_handler=image_processing_handler,
                              line_1_selection=p_line_1_selection,
                              line_2_selection=p_line_2_selection,
                              search_accuracy=p_search_accuracy,
                              minLineLength_1=p_minLineLength_1,
                              minLineLength_2=p_minLineLength_2,
                              logger = vision_node.get_logger())
                              
    if image_processing_handler.get_vision_ok():
      vision_node.get_logger().info('Vision process executed cleanly!')
    else:
      vision_node.get_logger().error('Vision process executed with error!')

  except ImageNotGrayScaleError as e:
    vision_node.get_logger().error(str(e))
    image_processing_handler.set_vision_ok(False)

  except ImageNotBinaryError as e:
    vision_node.get_logger().error(str(e))
    image_processing_handler.set_vision_ok(False)

  except Exception as e:
    vision_node.get_logger().fatal("Fatal Error in vision function! Contact maintainer!")
    vision_node.get_logger().fatal(e)
  
  #finally: 
  image_processing_handler.init_results()
  return image_processing_handler.get_display_image(), image_processing_handler.get_results()
  

if __name__ == '__main__':
  pass

