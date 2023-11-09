# Import the necessary libraries
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import json
from ament_index_python.packages import get_package_share_directory
import numpy as np
import os
from os import listdir
from datetime import datetime
import yaml
import fnmatch
from yaml.loader import SafeLoader
import subprocess
from ament_index_python.packages import get_package_share_directory
import math
from math import pi
import time
from pathlib import Path

from pm_vision_manager.va_py_modules.vision_utils import image_resize, degrees_to_rads, rads_to_degrees, get_screen_resolution, rotate_image
 
def process_image(self,received_frame,_process_pipeline_list):
    self.img_width  = received_frame.shape[1]
    self.img_height = received_frame.shape[0]
    self.FOV_width=self.umPROpixel*self.img_width 
    self.FOV_height=self.umPROpixel*self.img_height
    self.ROI_used=False
    print("FOV width is " + str(self.FOV_width) + "um")
    print("FOV hight is " + str(self.FOV_height) + "um")    
    frame_buffer=[]
    frame_processed = received_frame
    frame_visual_elements = np.zeros((received_frame.shape[0], received_frame.shape[1], 3), dtype = np.uint8)
    display_frame=received_frame
    frame_buffer.append(received_frame)
    self.VisionOK = True
    vision_results_file_dict={}
    vision_results_list=[]
    try:
      pipeline_list=_process_pipeline_list
      for list_item in pipeline_list:
      # Iterating through the json
        for key, function_parameter in list_item.items():
          match key:
            case "Set_camera_exposure_time":
              active = function_parameter['active']
              value = function_parameter['value']
              if active and not self.cross_val_running:
                self.set_camera_exposure_time(value)  
              break
                            
            case "threshold":
              active = function_parameter['active']
              thresh = function_parameter['thresh']
              maxval = function_parameter['maxval']
              type = function_parameter['type'] 
              if active:
                  _Command = "cv2." + type
                  _,frame_processed = cv2.threshold(frame_processed,thresh,maxval,exec(_Command))
                  print("Theshold executed")
                  display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                  frame_buffer.append(frame_processed)
            case "adaptiveThreshold":
                active = function_parameter['active']
                maxValue = function_parameter['maxValue']
                adaptiveMethod = function_parameter['adaptiveMethod']
                thresholdType = function_parameter['thresholdType']
                blockSize = function_parameter['blockSize'] 
                C_Value = function_parameter['C']
                if active:
                    _Command_adaptiveMethod = "cv2." + adaptiveMethod
                    _Command_thresholdType = "cv2." + thresholdType
                    frame_processed = cv2.adaptiveThreshold(frame_processed,maxValue,exec(_Command_adaptiveMethod),exec(_Command_thresholdType),blockSize,C_Value)
                    print("Adaptive Theshold executed")
                    display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                    frame_buffer.append(frame_processed)
            case "bitwise_not":
                active = function_parameter['active']
                if active:
                    frame_processed = cv2.bitwise_not(frame_processed)
                    print("bitwise_not executed")
                    display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                    frame_buffer.append(frame_processed)

            case "BGR2GRAY":
                active = function_parameter['active']
                if active:
                  if len(frame_processed.shape)==3:
                    frame_processed = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2GRAY)
                    display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                    frame_buffer.append(frame_processed)
                    print("BGR2GRAY executed")
                  else:
                    print("BGR2GRAY ignored! Image is already Grayscale!")

            case "ROI":
                active = function_parameter['active']
                if active:
                  if not self.ROI_used:
                    ROI_center_x_c = function_parameter['ROI_center_x']
                    ROI_center_y_c = function_parameter['ROI_center_y']
                    ROI_height = function_parameter['ROI_height']
                    ROI_width = function_parameter['ROI_width']
                    ROI_center_x_i, ROI_center_y_i = self.CS_Camera_TO_Image(ROI_center_x_c,ROI_center_y_c)
                    ROI_center_x_pix, ROI_center_y_pix = self.CS_Image_TO_Pixel(ROI_center_x_i, ROI_center_y_i)
                    ROI_half_height_pix = int(round(self.pixelPROum*ROI_height/2))
                    ROI_half_width_pix = int(round(self.pixelPROum*ROI_width/2))
                    ROI_top_left_x_pix = ROI_center_x_pix - ROI_half_width_pix
                    ROI_bottom_right_x_pix = ROI_center_x_pix + ROI_half_width_pix
                    ROI_top_left_y_pix = ROI_center_y_pix + ROI_half_height_pix
                    ROI_bottom_right_y_pix = ROI_center_y_pix - ROI_half_height_pix
                    self.ROI_CS_CV_top_left_x, self.ROI_CS_CV_top_left_y = self.CS_Conv_Pixel_Center_TO_Top_Left(frame_processed.shape[1], frame_processed.shape[0], ROI_top_left_x_pix, ROI_top_left_y_pix)
                    self.ROI_CS_CV_bottom_right_x, self.ROI_CS_CV_bottom_right_y = self.CS_Conv_Pixel_Center_TO_Top_Left(frame_processed.shape[1], frame_processed.shape[0], ROI_bottom_right_x_pix, ROI_bottom_right_y_pix)
                    if self.ROI_CS_CV_top_left_x>0 and self.ROI_CS_CV_top_left_y>0 and self.ROI_CS_CV_bottom_right_x <= self.img_width and self.ROI_CS_CV_bottom_right_y <= self.img_height:
                      frame_processed = frame_processed[self.ROI_CS_CV_top_left_y:self.ROI_CS_CV_bottom_right_y, self.ROI_CS_CV_top_left_x:self.ROI_CS_CV_bottom_right_x]
                      self.ROI_used = True
                      cv2.rectangle(frame_visual_elements,(self.ROI_CS_CV_top_left_x,self.ROI_CS_CV_top_left_y),(self.ROI_CS_CV_bottom_right_x,self.ROI_CS_CV_bottom_right_y),(240,32,160),3)
                      display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                      print("ROI executed")
                    else:
                      self.VisionOK=False
                      self.vision_node.get_logger().error('ROI failed! Out of bounds')
                  else:
                    self.vision_node.get_logger().warning('ROI already used! ROI can only be applied once!')                

            case "Canny":
              active = function_parameter['active']
              threshold1 = function_parameter['threshold1']
              threshold2 = function_parameter['threshold2']
              aperatureSize = function_parameter['aperatureSize']
              L2gradient = function_parameter['L2gradient'] 
              if active:
                  frame_processed = cv2.Canny(frame_processed,threshold1,threshold2,aperatureSize)
                  print("Canny executed")
                  display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                  frame_buffer.append(frame_processed)

            case "findContours":
              active = function_parameter['active']
              draw_contours = function_parameter['draw_contours']
              mode = function_parameter['mode']
              method = function_parameter['method']
              fill = function_parameter['fill']
              if active:
                  _Command_mode = "cv2." + mode
                  _Command_method = "cv2." + method
                  #contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), exec(_Command_method))  # Keine Ahnung warum das nicht funktioniert!!!
                  #print(_Command_method)
                  contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), cv2.CHAIN_APPROX_SIMPLE)
                  if fill:
                    cv2.fillPoly(frame_processed,pts=contours,color=(255,255,255))
                    display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                    frame_buffer.append(frame_processed)
                  if draw_contours:
                    cv2.drawContours(frame_visual_elements, contours, -1, (0,255,75), 2)
                  print("findContours executed")
            case "minEnclosingCircle":
              active = function_parameter['active']
              draw_circles = function_parameter['draw_circles']
              mode = function_parameter['mode']
              method = function_parameter['method']
              if active:
                try:
                  contours,hierarchy = cv2.findContours(frame_processed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                  print("Number of contours detected:", len(contours))
                  # select the first contour
                  cnt = contours[0]
                  (x_tl_roi, y_tl_roi),radius = cv2.minEnclosingCircle(cnt)
                  x_cs_camera, y_cs_camera = self.CS_CV_TO_camera_with_ROI(int(round(x_tl_roi)),int(round(y_tl_roi)))
                  radius_um=radius*self.umPROpixel
                  print(str(self.camera_axis_1)+'-Coordinate:'+ str(x_cs_camera))
                  print(str(self.camera_axis_2)+'-Coordinate:'+ str(y_cs_camera))
                  print('Radius: '+ str(radius_um))
                  Circle_result_dict={"Circle":{
                    'axis_1': x_cs_camera,
                    'axis_2': y_cs_camera,
                    'axis_1_suffix': self.camera_axis_1,
                    'axis_2_suffix': self.camera_axis_2,
                    "radius":radius_um,
                    "Unit": "um"
                    }}
                  if draw_circles:
                    x_tl,y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(int(round(x_tl_roi)),int(round(y_tl_roi)))
                    # Draw the circumference of the circle.

                    cv2.circle(frame_visual_elements, (x_tl, y_tl), int(round(radius)), (0, 255, 0), 2)
                    # Draw a small circle (of radius 1) to show the center.
                    cv2.circle(frame_visual_elements, (x_tl, y_tl), 1, (0, 0, 255), 2)
                  vision_results_list.append(Circle_result_dict)
                  print("minEnclosingCircle executed")
                except:
                  self.VisionOK=False
                  self.vision_node.get_logger().error('Min Enclosing Circle detection failed! Image may not be grayscale!')
            
            case "HoughLinesP":
              active = function_parameter['active']
              threshold = function_parameter['threshold']
              minLineLength = function_parameter['minLineLength']
              maxLineGap = function_parameter['maxLineGap']              
              if active:
                HoughLinesP_results_list=[]
                #print(type(HoughLinesP_results_list))
                lines = cv2.HoughLinesP(frame_processed,rho = 1,theta = 1*np.pi/180,threshold = threshold,minLineLength = minLineLength,maxLineGap = maxLineGap)
                if lines is not None:
                  for x1,y1,x2,y2 in lines[0]:
                    x1,y1 = self.CS_Conv_ROI_Pix_TO_Img_Pix(x1,y1)
                    x2,y2 = self.CS_Conv_ROI_Pix_TO_Img_Pix(x2,y2)
                    cv2.line(frame_visual_elements,(x1,y1),(x2,y2),(0,255,0),2)

                    x1_cs_camera, y1_cs_camera = self.CS_CV_TO_camera_with_ROI(x1,y1)
                    x2_cs_camera, y2_cs_camera = self.CS_CV_TO_camera_with_ROI(x2,y2)

                    print('Point 1 - ' + str(self.camera_axis_1)+'-Coordinate:'+ str(x1_cs_camera))
                    print('Point 1 - ' + str(self.camera_axis_2)+'-Coordinate:'+ str(y1_cs_camera))
                    print('Point 2 - ' + str(self.camera_axis_1)+'-Coordinate:'+ str(x2_cs_camera))
                    print('Point 2 - ' + str(self.camera_axis_2)+'-Coordinate:'+ str(y2_cs_camera))

                    HoughLinesP_results_list.append({
                      'Point_1': {'axis_1': x1_cs_camera,"axis_2":y2_cs_camera},
                      'Point_2': {'axis_1': x2_cs_camera,"axis_2":y2_cs_camera},
                      'axis_1_suffix': self.camera_axis_1,
                      'axis_2_suffix': self.camera_axis_2,
                      'angle': "to be added",
                      'length': "to be added",
                      "Unit": "um",
                      "angle_unit": "degree"
                      })

                  #print(HoughLinesP_results_list)
                  HoughLinesP_results_dict={"Lines": HoughLinesP_results_list}
                  vision_results_list.append(HoughLinesP_results_dict)
                  print(vision_results_list)
                    
                else:
                  self.VisionOK=False
                  self.vision_node.get_logger().error('No Line detected!')
                print("HoughLinesP executed")

            case "select_Area":
              active = function_parameter['active']
              mode = function_parameter['mode']
              method = function_parameter['method']
              max_area = function_parameter['max_area']
              min_area = function_parameter['min_area']
              if active:
                  _Command_mode = "cv2." + mode
                  _Command_method = "cv2." + method
                  #contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), exec(_Command_method))  # Keine Ahnung warum das nicht funktioniert!!!
                  contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), cv2.CHAIN_APPROX_SIMPLE)
                  all_areas= []
                  for cnt in contours:
                      area= cv2.contourArea(cnt)
                      all_areas.append(area)
                  contour_frame = np.zeros((frame_processed.shape[0], frame_processed.shape[1]), dtype = np.uint8)
                  self.VisionOK = False
                  for index, area_item in enumerate(all_areas):
                      
                      if area_item<max_area and area_item>min_area:
                        frame_processed = cv2.drawContours(contour_frame, contours, index, color=(255,255,255), thickness=cv2.FILLED)
                        self.VisionOK = True
                                    
                  if not self.VisionOK:
                    self.VisionOK = False
                    frame_processed = np.zeros((frame_processed.shape[0], frame_processed.shape[1]), dtype = np.uint8)
                    self.vision_node.get_logger().error("Select Area: No matching area")
                  display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                  frame_buffer.append(frame_processed)
                  print("select_Area executed")

            case "Morphology_Ex_Opening":
              active = function_parameter['active']
              kernelsize = function_parameter['kernelsize']
  
              if active:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
                frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_OPEN, kernel)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Morphology_Ex_Opening executed")

            case "Morphology_Ex_Closing":
              active = function_parameter['active']
              kernelsize = function_parameter['kernelsize']
  
              if active:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
                frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_CLOSE, kernel)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Morphology_Ex_Closing executed")
            
            case "Horizontal":
              active = function_parameter['active']
              h_kernelsize = function_parameter['h_kernelsize']
  
              if active:
                horizontal_size = received_frame.shape[1] // h_kernelsize
                horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
                frame_processed = cv2.erode(frame_processed, horizontalStructure)
                frame_processed = cv2.dilate(frame_processed, horizontalStructure)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Horizontal executed")

            case "Vertical":
              active = function_parameter['active']
              v_kernelsize = function_parameter['v_kernelsize']
  
              if active:
                vertical_size = received_frame.shape[0] // v_kernelsize
                verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
                frame_processed = cv2.erode(frame_processed, verticalStructure)
                frame_processed = cv2.dilate(frame_processed, verticalStructure)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Horizontal executed")

            case "Blur":
              active = function_parameter['active']
              kernelsize = function_parameter['kernelsize']
              blur_type = function_parameter['type']
  
              if active:
                if blur_type == "GaussianBlur":
                  frame_processed = cv2.GaussianBlur(frame_processed, (kernelsize, kernelsize),0)
                elif blur_type == "Blur":
                  frame_processed = cv2.blur(frame_processed, (kernelsize, kernelsize))
                elif blur_type == "medianBlur":
                  frame_processed = cv2.medianBlur(frame_processed, kernelsize)
                else:
                  self.vision_node.get_logger().error('Blur type not supported!')
                  self.VisionOK = False

                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Blur executed")                

            case "Morphology_Ex_Gradient":
              active = function_parameter['active']
              kernelsize = function_parameter['kernelsize']
  
              if active:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
                frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_GRADIENT, kernel)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Morphology_Ex_Gradient executed")

            case "Errosion":
              active = function_parameter['active']
              kernelsize = function_parameter['kernelsize']
              iterations = function_parameter['iterations']
  
              if active:
                kernel = np.ones((kernelsize, kernelsize), np.uint8)
                frame_processed = cv2.erode(frame_processed, kernel, iterations=iterations)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Errosion executed")

            case "Dilation":
              active = function_parameter['active']
              kernelsize = function_parameter['kernelsize']
              iterations = function_parameter['iterations']
  
              if active:
                kernel = np.ones((kernelsize, kernelsize), np.uint8)
                frame_processed = cv2.dilate(frame_processed, kernel, iterations=iterations)
                display_frame=self.adaptImagewithROI(display_frame,frame_processed)
                frame_buffer.append(frame_processed)
                print("Dilation executed")

            case "save_image":
              active = function_parameter['active']
              prefix = function_parameter['prefix']
              with_vision_elements = function_parameter['with_vision_elements']
              save_in_cross_val = function_parameter['save_in_cross_val']
              if active:
                  
                  if not os.path.exists(self.process_db_path):
                    os.makedirs(self.process_db_path)
                    print("Process DB folder created!")
                  
                  image_name=self.process_db_path+"/"+self.vision_process_id+"_"+self.process_start_time+prefix+".png"

                  if not os.path.isfile(image_name) and (not self.cross_val_running or save_in_cross_val):
                    if with_vision_elements:
                      display_frame = self.adaptImagewithROI(display_frame,frame_processed)
                      image_to_save = self.create_vision_element_overlay(display_frame,frame_visual_elements)
                    else:
                        image_to_save = frame_processed
                    cv2.imwrite(image_name,image_to_save)
                    print("Image saved!")

                  if (not self.cross_val_running or save_in_cross_val):
                    Save_image_results_dict={"Image saved:": image_name}
                    vision_results_list.append(Save_image_results_dict)

                  print("save_image executed")
                    
            case "Draw_Grid_without_rotation":
              active = function_parameter['active']
              grid_spacing = function_parameter['grid_spacing']
              if active:
                  numb_horizontal = int(round((self.FOV_height/2)/grid_spacing))+1
                  numb_vertical = int(round((self.FOV_width/2)/grid_spacing))+1
                  cv2.putText(img=frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)

                  cv2.line(frame_visual_elements, (int(display_frame.shape[1]/2), 0),(int(display_frame.shape[1]/2), display_frame.shape[1]), (255, 0, 0), 1, 1)
                  cv2.line(frame_visual_elements, (0,int(display_frame.shape[0]/2)),(int(display_frame.shape[1]), int(display_frame.shape[0]/2)), (255, 0, 0), 1, 1)
                  #Draw horizontal lines
                  for numb_h in range(numb_horizontal):
                    pixel_delta=int(numb_h*grid_spacing*self.pixelPROum)
                    cv2.line(frame_visual_elements, (0,int(display_frame.shape[0]/2)+pixel_delta),(int(display_frame.shape[1]), int(display_frame.shape[0]/2)+pixel_delta), (255, 0, 0), 1, 1)
                    cv2.line(frame_visual_elements, (0,int(display_frame.shape[0]/2)-pixel_delta),(int(display_frame.shape[1]), int(display_frame.shape[0]/2)-pixel_delta), (255, 0, 0), 1, 1)
                  # draw vertical lines
                  for numb_v in range(numb_vertical):
                    pixel_delta=int(numb_v*grid_spacing*self.pixelPROum)
                    cv2.line(frame_visual_elements, (int(display_frame.shape[1]/2)+pixel_delta, 0),(int(display_frame.shape[1]/2)+pixel_delta, display_frame.shape[1]), (255, 0, 0), 1, 1)
                    cv2.line(frame_visual_elements, (int(display_frame.shape[1]/2)-pixel_delta, 0),(int(display_frame.shape[1]/2)-pixel_delta, display_frame.shape[1]), (255, 0, 0), 1, 1)
                  print("Grid executed")

            case "Draw_Grid":
              active = function_parameter['active']
              grid_spacing = function_parameter['grid_spacing']
              
              if active:
                Grid_frame = np.zeros((received_frame.shape[0]+received_frame.shape[1], received_frame.shape[0]+received_frame.shape[1], 3), dtype = np.uint8)
                #numb = int(round((Grid_frame.shape[0]/2)/grid_spacing*self.pixelPROum))+1 # This is a bug
                numb = int(round((self.FOV_width/2)/grid_spacing))+1

                cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2), 0),(int(Grid_frame.shape[1]/2), Grid_frame.shape[1]), (255, 0, 0), 1, 1)
                cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)), (255, 0, 0), 1, 1)
                
                for n in range(numb):
                  #Draw horizontal lines
                  pixel_delta=int(n*grid_spacing*self.pixelPROum)
                  cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)+pixel_delta),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)+pixel_delta), (255, 0, 0), 1, 1)
                  cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)-pixel_delta),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)-pixel_delta), (255, 0, 0), 1, 1)
                  # draw vertical lines
                  cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2)+pixel_delta, 0),(int(Grid_frame.shape[1]/2)+pixel_delta, Grid_frame.shape[1]), (255, 0, 0), 1, 1)
                  cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2)-pixel_delta, 0),(int(Grid_frame.shape[1]/2)-pixel_delta, Grid_frame.shape[1]), (255, 0, 0), 1, 1)
                  
                Grid_frame= rotate_image(Grid_frame,self.camera_axis_1_angle)
                center = Grid_frame.shape
                x = center[1]/2 - self.img_width/2
                y = center[0]/2 - self.img_height/2

                crop_img = Grid_frame[int(y):int(y+self.img_height), int(x):int(x+self.img_width)]
                frame_visual_elements = self.create_vision_element_overlay(frame_visual_elements,crop_img)
                cv2.putText(img=frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)
                print("Grid executed")

            case "Draw_CS":
              active = function_parameter['active']
              if active:
                # Does not work for alpha >90 yet
                CS_frame = np.zeros((received_frame.shape[0]+received_frame.shape[1], received_frame.shape[0]+received_frame.shape[1], 3), dtype = np.uint8)
                if self.camera_axis_1 == 'z' or self.camera_axis_1 == 'Z':
                  color_axis_1 = (255, 0, 0)
                elif self.camera_axis_1 == 'y' or self.camera_axis_1 == 'Y':
                  color_axis_1 = (0, 255, 0)
                else:
                  color_axis_1 = (0, 0, 255)

                if self.camera_axis_2 == 'z' or self.camera_axis_2 == 'Z':
                  color_axis_2 = (255, 0, 0)
                elif self.camera_axis_2 == 'x' or self.camera_axis_2 == 'X':
                  color_axis_2 = (0, 0, 255)
                else:
                  color_axis_2 = (0, 255, 0)

                #draw axis_1
                cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(CS_frame.shape[1], int(CS_frame.shape[0]/2)), color_axis_1, 2, 1)
                #draw axis_2
                if self.camera_axis_2_angle == '+':
                  cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(int(CS_frame.shape[1]/2), 0), color_axis_2, 2, 1)
                else:
                  cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(int(CS_frame.shape[1]/2), CS_frame.shape[0]), color_axis_2 , 2, 1)
                CS_frame= rotate_image(CS_frame,self.camera_axis_1_angle)
                center = CS_frame.shape
                x = center[1]/2 - self.img_width/2
                y = center[0]/2 - self.img_height/2
                crop_img = CS_frame[int(y):int(y+self.img_height), int(x):int(x+self.img_width)]
                frame_visual_elements = self.create_vision_element_overlay(frame_visual_elements,crop_img)
                print("Draw_CS executed!")

            case "Draw_Grid_TO_BE_DELETED":
              active = function_parameter['active']
              grid_spacing = function_parameter['grid_spacing']
              
              if active:
                numb_horizontal = int(round((self.FOV_height/2)/grid_spacing))+1
                numb_vertical = int(round((self.FOV_width/2)/grid_spacing))+1
                cv2.putText(img=frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)

                # vertical center line
                p_x_centerline=-1*int(round(math.tan(degrees_to_rads(self.camera_axis_1_angle))*round(display_frame.shape[0]/2)))
                p_y_centerline=int(round(display_frame.shape[0]/2))
                p1_x_v_centerline_tl, p1_y_v_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],p_x_centerline,p_y_centerline)
                p2_x_v_centerline_tl, p2_y_v_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],-p_x_centerline,-p_y_centerline)
                cv2.line(frame_visual_elements, (p1_x_v_centerline_tl, p1_y_v_centerline_tl),(p2_x_v_centerline_tl, p2_y_v_centerline_tl), (255, 0, 0), 1, 1)
                
                # horizontal center line
                p_y_centerline=int(round(math.tan(degrees_to_rads(self.camera_axis_1_angle))*round(display_frame.shape[1]/2)))
                p_x_centerline=int(round(display_frame.shape[1]/2))
                p1_x_h_centerline_tl, p1_y_h_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],p_x_centerline,p_y_centerline)
                p2_x_h_centerline_tl, p2_y_h_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],-p_x_centerline,-p_y_centerline)
                cv2.line(frame_visual_elements, (p1_x_h_centerline_tl, p1_y_h_centerline_tl),(p2_x_h_centerline_tl, p2_y_h_centerline_tl), (255, 0, 0), 1, 1)
                
                # draw horizontal lines
                grid_spacing_t = int(round(math.cos(degrees_to_rads(self.camera_axis_1_angle))*grid_spacing*self.pixelPROum))

                for numb_h in range(numb_horizontal):
                  cv2.line(frame_visual_elements, (p1_x_h_centerline_tl, p1_y_h_centerline_tl+numb_h*grid_spacing_t),(p2_x_h_centerline_tl, p2_y_h_centerline_tl+numb_h*grid_spacing_t), (255, 0, 0), 1, 1)
                  cv2.line(frame_visual_elements, (p1_x_h_centerline_tl, p1_y_h_centerline_tl-numb_h*grid_spacing_t),(p2_x_h_centerline_tl, p2_y_h_centerline_tl-numb_h*grid_spacing_t), (255, 0, 0), 1, 1)
                # draw vertical lines
                for numb_v in range(numb_vertical):
                  pixel_delta=int(numb_v*grid_spacing*self.pixelPROum)
                  cv2.line(frame_visual_elements, (p1_x_v_centerline_tl+grid_spacing_t*numb_v, p1_y_v_centerline_tl),(p2_x_v_centerline_tl+grid_spacing_t*numb_v, p2_y_v_centerline_tl), (255, 0, 0), 1, 1)
                  cv2.line(frame_visual_elements, (p1_x_v_centerline_tl-grid_spacing_t*numb_v, p1_y_v_centerline_tl),(p2_x_v_centerline_tl-grid_spacing_t*numb_v, p2_y_v_centerline_tl), (255, 0, 0), 1, 1)
                print("Grid executed2")

            case "HoughCircles":
                active = function_parameter['active']
                draw_circles = function_parameter['draw_circles']
                method = function_parameter['method']
                dp = function_parameter['dp']
                minDist = function_parameter['minDist']
                param1 = function_parameter['param1']
                param2 = function_parameter['param2']
                minRadius = int(round(function_parameter['minRadius']* self.pixelPROum)) # conv in Pixel
                maxRadius = int(round(function_parameter['maxRadius']* self.pixelPROum)) # conv in Pixel
                if active:
                  _Command_method = "cv2." + method
                  #print(_Command_method)
                  try:
                    detected_circles = cv2.HoughCircles(frame_processed,cv2.HOUGH_GRADIENT, dp, minDist, param1 = param1,param2 = param2, minRadius = minRadius, maxRadius = maxRadius)
                    if detected_circles is not None:
                      print("Cirlces Detected")
                      # Convert the circle parameters a, b and r to integers.
                      detected_circles = np.uint16(np.around(detected_circles))
                      HoughCircles_reslults_list=[]
                      for pt in detected_circles[0, :]:
                        x, y, r = pt[0], pt[1], pt[2]

                        x_cs_camera, y_cs_camera = self.CS_CV_TO_camera_with_ROI(x,y)
                        radius_um=r*self.umPROpixel
                        print(str(self.camera_axis_1)+'-Coordinate:'+ str(x_cs_camera))
                        print(str(self.camera_axis_2)+'-Coordinate:'+ str(y_cs_camera))
                        print('Radius: '+ str(radius_um))
                        HoughCircles_reslults_list.append({
                          'axis_1': x_cs_camera,
                          'axis_2': y_cs_camera,
                          'axis_1_suffix': self.camera_axis_1,
                          'axis_2_suffix': self.camera_axis_2,
                          "radius":radius_um,
                          "Unit": "um"
                          })

                        if draw_circles:
                          x_tl,y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(x,y)
                          # Draw the circumference of the circle.
                          cv2.circle(frame_visual_elements, (x_tl, y_tl), r, (0, 255, 0), 2)
                          # Draw a small circle (of radius 1) to show the center.
                          cv2.circle(frame_visual_elements, (x_tl, y_tl), 1, (0, 0, 255), 2)
                      HouchCircles_results_dict={"Circles": HoughCircles_reslults_list}
                      vision_results_list.append(HouchCircles_results_dict)
                    else:
                      self.VisionOK=False
                      
                      self.vision_node.get_logger().error('No circle detected!')
                    print("Hough Circles executed")
                  except:
                    self.VisionOK=False
                    self.vision_node.get_logger().error('Circle detection failed! Image may not be grayscale!')

      if self.VisionOK:
        self.vision_node.get_logger().info('Vision process executed cleanly!')
      else:
        self.vision_node.get_logger().error('Vision process executed with error!')
        self.counter_error_cross_val += 1
    except Exception as e:
        self.vision_node.get_logger().error("Fatal Error in vision function! Contact maintainer!")
        self.vision_node.get_logger().error(e)
    
    if not self.VisionOK:
      cv2.rectangle(frame_visual_elements,(0,0),(frame_visual_elements.shape[1],frame_visual_elements.shape[0]),(0,0,255),3)
    else:
      cv2.rectangle(frame_visual_elements,(0,0),(frame_visual_elements.shape[1],frame_visual_elements.shape[0]),(0,255,0),3)
    
    # Add the vision_results_list to the vision_results_file
    vision_results_file_dict = {}
    vision_results_file_dict["vision_results"] = vision_results_list

    # Save the vision_results_file
    self.save_vision_results(vision_results_file_dict)

    display_frame=self.create_vision_element_overlay(display_frame,frame_visual_elements)

    if len(received_frame.shape)<3:
      received_frame = cv2.cvtColor(received_frame,cv2.COLOR_GRAY2BGR)

    if  self.show_input_and_output_image:
      display_frame = cv2.vconcat([received_frame,display_frame])

    display_frame=image_resize(display_frame, height = (self.screen_height-100))
    
    #time.sleep(4)

    return display_frame
  

if __name__ == '__main__':
  pass
