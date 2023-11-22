# Import the necessary libraries
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import json
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
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
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
from pathlib import Path
import sys
from pm_vision_manager.va_py_modules.vision_processes import process_image
from pm_vision_manager.va_py_modules.vision_utils import image_resize, degrees_to_rads, rads_to_degrees, get_screen_resolution, rotate_image
from functools import partial

from pm_vision_interfaces.srv import ExecuteVision
from pm_vision_interfaces.srv import StopVisionAssistant
from pm_vision_interfaces.srv import StartVisionAssistant
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass

class VisionNode(Node):
  """
  Create an ImagePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    super().__init__('vision_assistant')
    
    self.callback_group = ReentrantCallbackGroup()
    self.callback_group_image_subscriptions = MutuallyExclusiveCallbackGroup()
    self.br = CvBridge()
    self.image_list=[]
    self.running_vision_assistants=[]
    self.execute_vision_srv = self.create_service(ExecuteVision, 'ExecuteVision', self.execute_vision,callback_group=self.callback_group)
    self.execute_vision_srv = self.create_service(StartVisionAssistant, 'StartVisionAssistant', self.start_vision_assistant,callback_group=self.callback_group)
    self.execute_vision_srv = self.create_service(StopVisionAssistant, 'StopVisionAssistant', self.stop_vision_assistant,callback_group=self.callback_group)
    self.timer = self.create_timer(0.5, self.display_image_callback, callback_group=self.callback_group)
    self.get_logger().info("Vision node started!")
    
  def execute_vision(self, request: ExecuteVision.Request , response: ExecuteVision.Response):
    VisionProcess = VisionProcessClass(
      self,
      launch_as_assistant=False,
      process_filename=request.process_filename,
      camera_config_filename=request.camera_config_filename,
      db_cross_val_only=request.db_cross_val_only,
      process_UID=request.process_uid,
      image_display_time_visualization=request.image_display_time,
      open_process_file=False,
      run_cross_validation= request.run_cross_validation,
      show_image_on_error = False,
      step_through_images = False
      )
    while(not VisionProcess.delete_this_object):
      time.sleep(0.5)

    response.success = VisionProcess.VisionOK
    response.process_uid = request.process_uid
    response.results_dict = str(VisionProcess.results_dict)
    response.results_path = str(VisionProcess.vision_results_path)
    del VisionProcess

    return response
  
  def start_vision_assistant(self, request: StartVisionAssistant.Request , response: StartVisionAssistant.Response):
    try:

      for tpl in self.running_vision_assistants:
        if tpl[0] == request.process_uid:
          self.get_logger().error(f'Vision Assistant cannot be launched because a process with id: {tpl[0]} is already running!')
          raise Exception
        
      VisionProcess = VisionProcessClass(
        self,
        launch_as_assistant=True,
        process_filename=request.process_filename,
        camera_config_filename=request.camera_config_filename,
        db_cross_val_only=request.db_cross_val_only,
        process_UID=request.process_uid,
        image_display_time_visualization=-1,
        open_process_file=request.open_process_file,
        run_cross_validation = request.run_cross_validation,
        show_image_on_error = request.show_image_on_error,
        step_through_images = request.step_through_images
        )
      
      self.running_vision_assistants.append((request.process_uid, VisionProcess))

      response.success = True
      response.process_uid = request.process_uid

    except Exception:
      response.success = False
    return response
  
  def stop_vision_assistant(self, request: StopVisionAssistant.Request , response: StopVisionAssistant.Response):
    #if request.process_uid in self.running_vision_assistants:
    response.success =  False
    for index, VisionInstance in enumerate(self.running_vision_assistants):
      if VisionInstance[0] == request.process_uid:
        VisionInstance[1].stop_image_subscription = True
        VisionInstance[1].set_display_time_for_exit()
        while(not VisionInstance[1].delete_this_object):
          time.sleep(0.5)
        del self.running_vision_assistants[index]
        self.get_logger().info(f'Vision Assistant: {request.process_uid} stoped!')
        response.success = True
        response.process_uid = request.process_uid
        break

    if not response.success:
      self.get_logger().error(f'Vision Assistant with ID {request.process_uid} does not exist!')

    return response
  
  def display_image_callback(self):
    for index, image_item in enumerate(self.image_list):
      # Access elements within the tuple
      name, image, display_time, start_time = image_item

      if not(display_time == 0) and (self.get_clock().now().nanoseconds/1e9 > start_time.nanoseconds/1e9+ display_time):
        del self.image_list[index]
        cv2.destroyWindow(name)
        self.get_logger().info(f'Closing image: {name}')

    for index, image_item in enumerate(self.image_list):
      # Access elements within the tuple
      name, image, display_time, start_time = image_item

      if not display_time == 0:
        window_name = name
        cv2.imshow(window_name, image)

    cv2.waitKey(1)

    if len(self.image_list)==0:
      cv2.destroyAllWindows()
    

def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  vision_node = VisionNode()
  executor = MultiThreadedExecutor(num_threads=6)
  executor.add_node(vision_node)

  # Spin the node so the callback function is called.
  executor.spin()
  
  executor.shutdown()
  vision_node.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
