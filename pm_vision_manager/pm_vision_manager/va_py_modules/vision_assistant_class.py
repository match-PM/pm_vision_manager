# Import the necessary libraries
from sensor_msgs.msg import Image  # Image is the message type
import cv2  # OpenCV library
import json
import os
from os import listdir
from datetime import datetime
import yaml
import fnmatch
from yaml.loader import SafeLoader
import subprocess
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
from math import pi
from rosidl_runtime_py.convert import message_to_ordereddict, get_message_slot_types
import time
from pynput import keyboard
from pathlib import Path
import threading
from rosidl_runtime_py.utilities import get_service #, get_interface, get_message
from pm_vision_manager.va_py_modules.vision_pipline_processing import process_image, set_camera_parameters
from threading import Thread
from rclpy.node import Node
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy, QoSHistoryPolicy, qos_profile_sensor_data
import numpy as np
from collections import OrderedDict
from rclpy.impl.rcutils_logger import RcutilsLogger
import gc
import copy

from PyQt6.QtCore import Qt, QByteArray, pyqtSignal, QObject

import pm_vision_interfaces.msg as pvimsg 
from pm_vision_manager.va_py_modules.camera_ros_interfaces import CameraRosInterfaces

SUPPORTED_TYPES = [".png", ".jpg", ".jpeg", ".bmp"]

class VisionCrossvalidation:
    def __init__(self, images_path):
        self.db_path = images_path
        # create the db folder if it does not exist
        self.init_db_folder()
        self.running = False
        self.has_been_executed = False
        self.failed_images = []
        self.counter_error = 0
        self.visionOK = True
        self.numb_images = 0
        self.images = []
        self.current_image_index = 0
        self.current_image_name = None
        self.init_images()

    def init_images(self):
        self.images = listdir(self.db_path)
        _filtered_images = []
        for ext in SUPPORTED_TYPES:
            _filtered_images.extend(fnmatch.filter(self.images, "*"+ext))
        self.images = _filtered_images
        
        #self.images = fnmatch.filter(self.images, "*.png")

        self.images.sort()
        self.numb_images = len(self.images)
        return self.images
    
    def init_db_folder(self):
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

    def reset_cross_val(self):
        self.failed_images.clear()
        self.counter_error = 0
        self.visionOK = True
        self.numb_images = 0
        self.images = []
        self.current_image_index = 0
        self.current_image_name = None
        self.init_images()

    def get_image_by_filename(self, filename:str)->np.ndarray:
        """
        Returns the image as a numpy array
        :param filename: The name of the image file
        :type filename: str
        :return: The image as a numpy array
        :rtype: np.ndarray
        """
        return cv2.imread(f"{self.db_path}/{filename}")
    
    def get_current_image(self)->np.ndarray:
        """
        Returns the current image as a numpy array
        :return: The current image as a numpy array
        :rtype: np.ndarray
        """

        return self.get_image_by_filename(self.images[self.current_image_index])
    
    def set_current_image(self, name:str):
        """
        Sets the current image by name
        :param name: The name of the image
        :type name: str
        """
        self.current_image_name = name
        self.current_image_index = self.images.index(name)

    def append_to_failed_images(self, image_name:str):
        """
        Appends the image name to the list of failed images
        :param image_name: The name of the image
        :type image_name: str
        """
        self.failed_images.append(image_name)
    
    def start_cross_val(self):
        self.running = True
    
    def stop_cross_val(self):
        self.running = False
    
    def check_cross_val_running(self):
        return self.running

    def get_error_count(self):
        return self.counter_error

    def get_total_number_images(self):
        return self.numb_images
    
    def get_images_names(self)->list:
        return self.images
    
    def get_failed_images(self)->list:
        return self.failed_images
    
    def get_crossval_image_info(self)->tuple[int, int]:
        """
        Returns the current image count and the total number of images in the cross validation folder
        :return: current_image_count, numb_images_cross_val
        :rtype: int, int
        """
        return self.current_image_index, self.get_total_number_images()
    
class VisionResultsSignal(QObject):
    signal = pyqtSignal(np.ndarray, dict)

class SetCrossValResultsSignal(QObject):
    signal = pyqtSignal(list)

class VisionProcessClass:
    """
    TBD
    """
    def __init__(
        self,
        vision_node: Node,
        process_filename:str,
        camera_config_filename:str,
        launch_as_assistant:bool = False,
        process_UID = 'VisionAssistant',
        run_cross_validation = False,
        ):

        self.vision_node = vision_node
        self.launch_as_assistant = launch_as_assistant
        self.process_filename = process_filename
        self.camera_config_filename = camera_config_filename
        self.process_UID = process_UID
        
        self.run_cross_validation = run_cross_validation

        self.processing_source = None
        self.timer_active = False
        self._current_frame = None
        self._vision_loop_thread = None

        self.br = CvBridge()
        self.ros_camera_interfaces = CameraRosInterfaces(self.vision_node)
        self.image_processing_handler = ImageProcessingHandler(self.vision_node.get_logger())

        # create the image processing handler for cross validation
        self.image_processing_handler_cross_val = ImageProcessingHandler(self.vision_node.get_logger())
        self.image_processing_handler_cross_val.set_cross_val_running(True)
        self.image_processing_handler_cross_val.set_mode(ImageProcessingHandler.MODE_CROSSVAL)

        package_share_directory = get_package_share_directory("pm_vision_manager")
        self.path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"

        if self.launch_as_assistant:
            self.vision_node.get_logger().info("Starting Vision Assistant!")
            self.image_processing_handler.set_mode(ImageProcessingHandler.MODE_LOOP)
        else:
            self.vision_node.get_logger().info("Execute Vision!")
            self.image_processing_handler.set_mode(ImageProcessingHandler.MODE_EXECUTE)

        self.vision_node.get_logger().info(f"Current vision process: {self.process_filename}")
        
        #self.process_start_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        #self.process_start_time_ms = self.vision_node.get_clock().now()

        path_load_success = self.load_path_config()
        load_config_success = self.load_assistant_config()
        load_meta_success = self.load_process_file_metadata()
        load_camera_success = self.load_camera_config()

        if not path_load_success:
            raise ValueError(f"Path configuration file '{self.path_config_path}' could not be loaded!")
        if not load_config_success:
            raise ValueError(f"Vision assistant configuration file '{self.vision_assistant_config_path}' could not be loaded!")
        if not load_meta_success:
            raise ValueError(f"Process file '{self.process_file_path}' could not be loaded!")
        if not load_camera_success:
            raise ValueError(f"Camera configuration file '{self.camera_config_path + self.camera_config_filename}' could not be loaded!")

        # set the signals        
        self.results_signal = VisionResultsSignal()
        self.set_crossval_results_signal = SetCrossValResultsSignal()

        self.cross_validation = VisionCrossvalidation(self.process_db_path)

        self.subscription_active = False
        self._delete_this_object = False     # This is only used in assist mode
        self.vision_results_path = "None"
        self.process_pipeline_list: list = []
        self.callback_group = MutuallyExclusiveCallbackGroup()
        self.callback_group_RE = ReentrantCallbackGroup()

    def set_processing_source(self, source:str):
        # this is set from outside the class, e.g. from the vision assistant app
        self.processing_source = source
    
    def _image_topic_watchdog(self):
        
        self.vision_node.get_logger().error("Timed out! Image topic not available! Exiting...")
        self._delete_this_object = True
        # This is needed for the response(success) of the service call
        self.image_processing_handler.set_vision_ok(False)
        self.vision_node.destroy_subscription(self.subscription)
        self.topic_timer.cancel()
        self.timer_active = False

    def _start_vision_subscription(self)->bool:
        self.subscription_active = True
        self.subscription = self.vision_node.create_subscription(
            Image,
            self.camera_subscription_topic,  # defined in camera_config.yaml
            self.topic_cbk,
            qos_profile=qos_profile_sensor_data,
            callback_group=self.callback_group_RE)
        self.subscription
        
        if not self.launch_as_assistant:
            self.vision_node.get_logger().info("Starting watchdog for image topic with timeout of 10s...")
            self.timer_active = True
            self.topic_timer = self.vision_node.create_timer(20, self._image_topic_watchdog, callback_group=self.callback_group_RE)

        return True
    
    def _stop_vision_subscription(self) -> bool:
        if self.subscription_active:
            self.vision_node.destroy_subscription(self.subscription)
            if not self.launch_as_assistant:
                self.topic_timer.cancel()
            self.subscription_active = False
            return True
    
    def start_vision_assistant(self):
        self._start_vision_subscription()
        #self.vision_loop_thread = Thread(target=self.vision_assistant_loop, daemon=True)
        #self.vision_loop_thread.start()
        #self.vision_node.get_logger().error("Vision Assistant started!")
        self.vision_assistant_loop()
    
    def execute_vision(self):
        self._start_vision_subscription()
        time.sleep(0.5)
        
        image_name = f"{self.process_UID}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"

        self._load_process_file()

        set_parameter_success = set_camera_parameters(self.vision_node, 
                                                      self.image_processing_handler,
                                                      self.process_pipeline_list)
        
        if not set_parameter_success:
            self.image_processing_handler.vision_routine_done = True
            self.image_processing_handler.visionOK = False
            return


        image = self._get_current_camera_image()

        while (self.timer_active and image is None):
            
            image = self._get_current_camera_image()
            self.vision_node.get_logger().info(f"No image on topic '/{self.camera_subscription_topic}' available! Waiting...")
            time.sleep(0.5)
            continue

            # if image is None:
            #     self.vision_node.get_logger().info(f"No image on topic '/{self.camera_subscription_topic}' available! Waiting...")
            #     time.sleep(0.5)
            #     continue
                        
    
        self.image_processing_handler.set_image_metatdata(self.process_db_path,image_name)
        self.image_processing_handler.set_initial_image(image)

        #display_image = process_image(self, image, self.process_pipeline_list)
        display_image, vision_results = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
        final_image = self.image_processing_handler.get_final_image()
        
        # save to json file
        _results = self.save_vision_results()
        self.results_signal.signal.emit(final_image, _results)

        # run this when the execution is finished     
        if self.run_cross_validation:
            self.execute_crossvalidation()
            # reinitilize the results after crossvalidation has been executed
            _results = self.save_vision_results()
            self.results_signal.signal.emit(final_image, _results)
        
        self.image_processing_handler.vision_routine_done = True

    def close_vision_assistant(self):
        self._delete_this_object = True
        
    def terminate_vision_class(self):
        """
        Stops subscriptions, deletes signals, and ensures threads and memory are cleaned.
        """
        self._stop_vision_subscription()
        
        # Stop running threads or loops if any
        #self._delete_this_object = True
        # Break signal references
        try:
            self.results_signal.signal.disconnect()
        except TypeError:
            pass
            #self.vision_node.get_logger().error("Results signal was not connected!")
        try:
            self.set_crossval_results_signal.signal.disconnect()
        except TypeError:
            pass
            #self.vision_node.get_logger().error("Set cross validation results signal was not connected!")
            
        del self.results_signal
        del self.set_crossval_results_signal
        # Clean up any cross references
        del self.image_processing_handler
        del self.image_processing_handler_cross_val
        del self.cross_validation
        del self.ros_camera_interfaces

        # Optional: help GC
        gc.collect()

    def topic_cbk(self, data):

        #self.vision_node.get_logger().info("Receiving video frame")
        # Convert ROS Image message to OpenCV image
        received_frame = self.br.imgmsg_to_cv2(data)
        
        # if image is not a greyscale image
        if not len(received_frame.shape) == 2:
            if received_frame.shape[2] == 4: # Check if it has an alpha channel - This is for unity
                received_frame = cv2.cvtColor(received_frame, cv2.COLOR_RGBA2BGR)

        self._current_frame = received_frame
    
    def _get_current_camera_image(self) -> np.ndarray:
        """
        Returns the current camera image as a numpy array.
        :return: The current camera image.
        :rtype: np.ndarray
        """
        if self._current_frame is not None:
            return (self._current_frame)
        else:
            #self.vision_node.get_logger().error("No current frame available!")
            return None


    # def topic_cbk(self, data):
    #     self.subscription_active = True
    #     self.topic_available = True
    #     self.image_processing_handler.stop_vision_execution = True
    #     self._load_process_file()

    #     self.vision_node.get_logger().info("Receiving video frame")
    #     # Convert ROS Image message to OpenCV image
    #     received_frame = self.br.imgmsg_to_cv2(data)

    #     #self.vision_node.get_logger().warn(f"{len(received_frame.shape)}")
        
    #     # if image is not a greyscale image
    #     if not len(received_frame.shape) == 2:

    #         if received_frame.shape[2] == 4: # Check if it has an alpha channel - This is for unity
    #             received_frame = cv2.cvtColor(received_frame, cv2.COLOR_RGBA2BGR)

    #     if self.launch_as_assistant:
    #         image_name = f"{self.process_UID}"
    #     else:
    #         image_name = f"{self.process_UID}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"

    #     self.image_processing_handler.set_image_metatdata(self.process_db_path,image_name)
    #     self.image_processing_handler.set_initial_image(received_frame)

    #     #display_image = process_image(self, received_frame, self.process_pipeline_list)
    #     display_image, vision_results = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
    #     final_image = self.image_processing_handler.get_final_image()
    #     # save to json file
    #     _results = self.save_vision_results()
    #     self.results_signal.signal.emit(final_image, _results)

    #     # this only runs in execution mode and when the execution is finished
    #     if not self.launch_as_assistant and self.image_processing_handler.stop_vision_execution:   # self.stop_vision_execution may be overwritten in process_image function
    #         if self.run_cross_validation:
    #             self.execute_crossvalidation()
    #             # reinitilize the results after crossvalidation has been executed
    #             _results = self.save_vision_results()
    #             self.results_signal.signal.emit(final_image, _results)
    #         self._stop_vision_subscription()
    #         self.image_processing_handler.vision_routine_done = True

    def vision_assistant_loop(self):

        while not self._delete_this_object:
            
            if self.processing_source is None:
                self.vision_node.get_logger().error("No image source selected!")
                time.sleep(0.5)
                continue

            if (self.processing_source == self.camera_subscription_topic):
                set_camera_parameter_success = set_camera_parameters(self.vision_node,
                                                        self.image_processing_handler,
                                                        self.process_pipeline_list)
            
                if not set_camera_parameter_success:
                    self.vision_node.get_logger().error(f"Error occured. Camera parameter could not be set!")
                    continue

                image = self._get_current_camera_image()

            else:
                image = self.cross_validation.get_image_by_filename(self.processing_source)
            
            if image is None:
                self.vision_node.get_logger().error(f"Image source '{self.processing_source}' is not available!")
                time.sleep(0.5)
                continue
                        
            self._process_image_for_widget(image, os.path.splitext(self.processing_source)[0])
            
            #time.sleep(0.5)
            #self.vision_node.get_logger().error("Looped!")

        self.vision_node.get_logger().error("Vision assistant loop terminated!")   
        self.image_processing_handler.disable_all_lights()
        self.terminate_vision_class()

    def execute_crossvalidation(self):
        # Starting cross validation with images in folder
        if self.cross_validation.check_cross_val_running():
            self.vision_node.get_logger().warn("Crossvalidation is currently running! Could not execute crossvalidation!")
            return
        
        self.cross_validation.start_cross_val()
        self.cross_validation.reset_cross_val()

        self.vision_node.get_logger().info("Starting crossvalidation...")

        if len(self.cross_validation.images) == 0:
            self.vision_node.get_logger().error("No images in DB yet!")

        self._load_process_file()

        for index, current_image_file in enumerate(self.cross_validation.images):
            
            # Set the filename without the extension
            self.cross_validation.current_image_name = os.path.splitext(current_image_file)[0]

            image = self.cross_validation.get_image_by_filename(current_image_file)    
            
            image_name = f"{self.cross_validation.current_image_name}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"
            self.image_processing_handler_cross_val.set_image_metatdata(self.process_db_path, image_name)
            self.image_processing_handler_cross_val.set_initial_image(image)
            display_image, _ = process_image(self.vision_node, self.image_processing_handler_cross_val, self.process_pipeline_list)
            
            self.save_vision_results()

            if not self.image_processing_handler_cross_val.get_vision_ok():
                self.cross_validation.visionOK = False
                self.cross_validation.append_to_failed_images(current_image_file)
                self.cross_validation.counter_error += 1
        
        self.cross_validation.has_been_executed = True
        # this signal is only used in execution mode. In assistant mode the signal has no effect
        self.set_crossval_results_signal.signal.emit(self.cross_validation.get_failed_images())
        self.vision_node.get_logger().info("Crossvalidation ended...")
        self.cross_validation.stop_cross_val()

    def _process_image_for_widget(self, image:np.ndarray, image_name:str=""):
        # this is only used in the vision assistant mode
        
        self._load_process_file()
        self.image_processing_handler.set_initial_image(image)
        self.image_processing_handler.set_image_metatdata(self.process_db_path, image_name)
        display_image, _ = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
        _results = self.save_vision_results()
        self.results_signal.signal.emit(self.image_processing_handler.get_final_image(), _results)
    

    def load_path_config(self) -> bool:
        try:
            with open(self.path_config_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["vision_assistant_path_config"]
            self.process_library_path = config["process_library_path"]
            self.vision_database_path = config["vision_database_path"]
            self.camera_config_path = config["camera_config_path"]
            package_share_dir = get_package_share_directory("pm_vision_manager")
            self.vision_assistant_config_path = f"{package_share_dir}/vision_assistant_config.yaml"
            self.process_file_path = self.process_library_path + self.process_filename
            self.vision_node.get_logger().info("Vision assistant path config loaded!")
            return True
        
        except Exception as e:
            self.vision_node.get_logger().error(f"Error opening vision assistant path configuration: '{str(self.path_config_path)}'! Error: {str(e)}")
            return False

    def load_assistant_config(self) -> bool:
        try:
            with open(self.vision_assistant_config_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["vision_assistant_config"]
            self.show_input_and_output_image = config["show_input_and_output_image"]
            self.scale_ouput_window_to_screen_size = config["scale_ouput_window_to_screen_size"]
            self.vision_node.get_logger().info("Vision assistant config loaded!")
            return True
        except Exception as e:
            self.vision_node.get_logger().error(f"Error opening vision assistant configuration: '{str(self.vision_assistant_config_path)}'! Error: {str(e)}!")
            return False

    # def start_vision_app(self):
    #     try:
    #         self.app_thread = threading.Thread(target=self.open_process_file_in_app)
    #         self.app_thread.start()
            
    #     except Exception as e:
    #         self.vision_node.get_logger().error(e)
    #         self.vision_node.get_logger().error("Process File could not be opened!")

    # def open_process_file_in_app(self):
    #     """
    #     THIS IS NOT USED ANYMORE!
    #     """

    #     try:
    #         arguments = [f"pipeline_file_path:{self.process_file_path}"]
    #         python_file_path = f"{get_package_prefix('pm_vision_app')}/lib/python3.10/site-packages/pm_vision_app/vision_assistant_app.py"
    #         command = ['python3', python_file_path] + arguments
    #         subprocess.run(command)
            
    #     except Exception as e:
    #         self.vision_node.get_logger().error(e)
    #         self.vision_node.get_logger().error("Process File could not be opened!")
    

    def load_camera_config(self) -> bool:
        try:
            with open(self.camera_config_path + self.camera_config_filename, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["camera_params"]
            self.camera_id = config["cameraname"]
            self.camera_subscription_topic = config["subscription_topic"]

            self.image_processing_handler.set_camera_parameter(pixelsize=config["pixelsize"],
                                                               magnification=config["magnification"],
                                                               camera_axis_1=config["camera_axis_1"],
                                                               camera_axis_2=config["camera_axis_2"],
                                                               camera_axis_1_angle=config["camera_axis_1_angle"],
                                                               camera_axis_2_angle=config["camera_axis_2_angle"])
            
            self.image_processing_handler_cross_val.set_camera_parameter(pixelsize=config["pixelsize"],
                                                                magnification=config["magnification"],
                                                                camera_axis_1=config["camera_axis_1"],
                                                                camera_axis_2=config["camera_axis_2"],
                                                                camera_axis_1_angle=config["camera_axis_1_angle"],
                                                                camera_axis_2_angle=config["camera_axis_2_angle"])

            self.ros_camera_interfaces.exposure_time_interface.init(config=config.get('exposure_time', {}))
            self.image_processing_handler.set_camera_exposure_time = self.ros_camera_interfaces.exposure_time_interface.set_camera_exposure_time
            
            self.ros_camera_interfaces.set_coax_light_bool_interface.init(config=config.get('set_coax_light_bool', {}))
            self.image_processing_handler.set_camera_coax_light_bool = self.ros_camera_interfaces.set_coax_light_bool_interface.set_coax_light

            self.ros_camera_interfaces.set_coax_light_interface.init(config=config.get('set_coax_light', {}))
            
            #if self.ros_camera_interfaces.set_coax_light_interface.available:
            self.image_processing_handler.set_camera_coax_light = self.ros_camera_interfaces.set_coax_light_interface.set_coax_light

            self.ros_camera_interfaces.set_ring_light_interfaces.init(config=config.get('ring_light', {}))
            
            #if self.ros_camera_interfaces.set_ring_light_interfaces.available:
            self.image_processing_handler.set_ring_light = self.ros_camera_interfaces.set_ring_light_interfaces.set_ring_light

            self.vision_node.get_logger().info("Camera config loaded!")
            return True
        except Exception as e:
            self.vision_node.get_logger().error(f"Error opening or error in camera config file: {str(self.camera_config_path + self.camera_config_filename)}! Error: {str(e)}")
            return False
                
    # def check_process_file_existence(self):
    #     if os.path.exists(self.process_file_path) == False:
    #         self.vision_node.get_logger().warning("Given Process File does not exist!")
    #         if self.launch_as_assistant:
    #             print(f"Should {self.process_file_path} be created?")
    #             print("Enter y/n to continue")
    #             while True:
    #                 a = input()
    #                 if a == "y":
    #                     self.create_process_file()
    #                     break
    #                 elif a == "n":
    #                     print("Process File will not be created!")
    #                     break
    #                 elif a == "exit":
    #                     print("Process File will not be created!")
    #                     break
    #                 else:
    #                     print("Enter either yes/no")
    
    # def create_process_file(self):
    #     try:
    #         default_process_file_metadata_dict = self.create_default_process_dict(self.process_filename)
    #         # Create folders if not existend
    #         Path(os.path.dirname(self.process_file_path)).mkdir(
    #             parents=True, exist_ok=True
    #         )
    #         with open(self.process_file_path, "w+") as outputfile:
    #             json.dump(default_process_file_metadata_dict, outputfile,indent=4)
    #     except Exception as e:
    #         print(e)
    #         self.vision_node.get_logger().error("Error creating process file")
    
    def load_process_file_metadata(self) -> bool:
        try:
            with open(self.process_file_path, "r") as file:
                FileData = json.load(file)
            
            self.vision_process_name = FileData["vision_process_name"]
            #default
            self.process_db_path = self.vision_database_path + self.process_filename.split('.json')[0] # default
            """ Braucht Niklas für seine MA """
            #self.process_db_path = self.vision_database_path # Einstellen über die config-file
            """"""
            self.vision_node.get_logger().info("Process meta data loaded!")
            return True
        except Exception as e:
            self.vision_node.get_logger().error(
                f"Error opening process file: {str(self.process_file_path)}! Error: {str(e)}"
            )
            return False

    def _load_process_file(self):
        try:
            with open(self.process_file_path, "r") as file:
                FileData = json.load(file)
            self.process_pipeline_list.clear()
            self.process_pipeline_list = FileData["vision_pipeline"]
            #self.vision_node.get_logger().info("Process pipeline loaded!")
        except Exception as e:
            self.vision_node.get_logger().error(
                f"Error opening process file: {str(self.process_file_path)}! Error: {str(e)}"
            )

    def save_vision_results(self)->dict:
        """
        The function add metadata to the results dict and saves it to a json file
        :param result_dict: The results of the vision process
        :type result_dict: dict
        :return: The results of the vision process
        :rtype: dict
        """
        #result_dict = self.construct_results_metadata2(result_dict)
        result_dict = self.ordered_dict_to_dict(message_to_ordereddict(self.construct_results_metadata(self.image_processing_handler.get_vision_response())))

        # Set path for results dict
        if not self.cross_validation.check_cross_val_running():
            vision_results_path = f"{self.process_library_path}{Path(self.process_file_path).stem}_results_{self.camera_id}.json"
            self.vision_results_path = (vision_results_path)  # needed for the service response
        else:
            #default
            results_folder_path = f"{self.vision_database_path}{self.process_filename.split('.json')[0]}/{self.camera_id}" # default
            vision_results_path = f"{results_folder_path}/results_{str(self.cross_validation.current_image_name)}.json" # default
            """ Braucht Niklas für seine MA """
            #results_folder_path = f"{self.process_library_path}{self.process_filename.split('Chromosom')[0]}"
            #vision_results_path = f"{results_folder_path}/results_{str(self.crossval_image_name)}.json"
            """"""

        ## Maybe we need this anymore

        #     if not os.path.exists(results_folder_path):
        #         os.makedirs(results_folder_path)
        #         print("Results folder crossval created!")

        # try:
        #     with open(vision_results_path, "w") as outputfile:
        #         json.dump(result_dict, outputfile,indent=4)
        # except:
        #     self.vision_node.get_logger().warn(f"Vision_results_path: {vision_results_path}")
        #     self.vision_node.get_logger().error("Error saving vision results!")

        return result_dict

    # def construct_results_metadata2(self, result_dict:dict)->dict:
    #     result_meta_dict = {}

    #     result_meta_dict["vision_process_name"] = self.process_filename
    #     result_meta_dict["exec_timestamp"] = str(
    #         datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    #     )
    #     result_meta_dict["vision_OK"] = self.image_processing_handler.get_vision_ok()
    #     result_meta_dict["process_UID"] = self.process_UID

    #     if self.cross_validation.check_cross_val_running():
    #         result_meta_dict["image_name"] = str(self.cross_validation.current_image_name)

    #     if self.cross_validation.has_been_executed and not self.cross_validation.check_cross_val_running():
    #         result_meta_dict["VisionOK_cross_val"] = self.cross_validation.visionOK
    #         result_meta_dict["failed_images_cross_val"] = self.cross_validation.failed_images
    #         result_meta_dict["total_images_cross_val"] = self.cross_validation.numb_images
    #         result_meta_dict["failed_images_count"] = self.cross_validation.counter_error

    #     # Insert metadata at the beginning of the dictionary
    #     result_dict = {**result_meta_dict, **result_dict}

    #     return result_dict

    def construct_results_metadata(self, vision_response: pvimsg.VisionResponse)->pvimsg.VisionResponse:

        vision_response.process_name = self.process_filename
        vision_response.exec_timestamp = str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))

        vision_response.process_uid = self.process_UID
        vision_response.vision_ok = self.image_processing_handler.get_vision_ok()

        if self.cross_validation.check_cross_val_running():
            vision_response.cross_validation.image_source_name = str(self.cross_validation.current_image_name)

        if self.cross_validation.has_been_executed and not self.cross_validation.check_cross_val_running():
            vision_response.cross_validation.vision_ok = self.cross_validation.visionOK
            vision_response.cross_validation.failed_images = self.cross_validation.failed_images
            vision_response.cross_validation.numb_images = self.cross_validation.numb_images
            vision_response.cross_validation.counter_error = self.cross_validation.counter_error

        return vision_response
    
    def ordered_dict_to_dict(self, ordered_dict:OrderedDict):
        if isinstance(ordered_dict, OrderedDict):
            return dict((key, self.ordered_dict_to_dict(value)) for key, value in ordered_dict.items())
        elif isinstance(ordered_dict, list):
            return [self.ordered_dict_to_dict(item) for item in ordered_dict]
        else:
            return ordered_dict
        
    @staticmethod
    def create_default_process_dict(process_name):
        default_process_file_metadata_dict = {}
        default_process_file_metadata_dict["vision_process_name"] = process_name
        default_process_file_metadata_dict["id_process"] = "default_ID"
        default_process_file_metadata_dict["File_created"] = str(
            datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        )
        default_process_file_metadata_dict["vision_pipeline"] = [
        {
            "VisionOkOverride": {
                "active": True,
                "override_vision_ok": False
            }
        }
        ]
        
        return default_process_file_metadata_dict
    
    @staticmethod
    def create_process_file(directory: str, process_name: str, logger: RcutilsLogger = None):
        try:
            # Generate default metadata and determine file paths
            default_process_file_metadata_dict = VisionProcessClass.create_default_process_dict(process_name)
            process_lib_dir = VisionProcessClass.get_process_database_path(logger)
            file_dir = os.path.join(process_lib_dir, directory)
            process_file_path = os.path.join(file_dir, f"{process_name}.json")

            # Create folder if it doesn't exist
            if not os.path.exists(file_dir):
                Path(file_dir).mkdir(parents=True, exist_ok=True)
                if logger is not None:
                    logger.info(f"Process folder '{file_dir}' created!")

            # Create JSON file only if it doesn't exist
            if not os.path.exists(process_file_path):
                with open(process_file_path, "w") as outputfile:
                    json.dump(default_process_file_metadata_dict, outputfile, indent=4)
                if logger is not None:
                    logger.info(f"Process file '{process_file_path}' created!")

        except Exception as e:
            if logger is not None:
                logger.error(f"Error creating process file: {str(e)}")
                
    @staticmethod
    def get_process_database_path(logger=None)->str:
        config_file_path = f"{get_package_share_directory('pm_vision_manager')}/vision_assistant_path_config.yaml"
        process_library_path = None
        with open(str(config_file_path), "r") as file:
            FileData = yaml.safe_load(file)
            config = FileData["vision_assistant_path_config"]
            process_library_path = config["process_library_path"]

        if logger is not None:
            logger.debug(f"Process library path: {process_library_path}")
        return process_library_path

    @staticmethod
    def get_camera_libary_path(logger=None)->str:
        config_file_path = f"{get_package_share_directory('pm_vision_manager')}/vision_assistant_path_config.yaml"
        camera_library_path = None
        with open(str(config_file_path), "r") as file:
            FileData = yaml.safe_load(file)
            config = FileData["vision_assistant_path_config"]
            camera_library_path = config["camera_config_path"]

        if logger is not None:
            logger.debug(f"Process library path: {camera_library_path}")
        return camera_library_path
        
    @staticmethod
    def create_process_folder(process_folder:str,logger=None):
        try:
            process_library_path = VisionProcessClass.get_process_database_path(logger)
            process_folder_path = f"{process_library_path}{process_folder}"
            if logger is not None:
                logger.info(f"Process folder '{process_folder_path}' created!")

            if not os.path.exists(process_folder_path):
                os.makedirs(process_folder_path)
                if logger is not None:
                    logger.info(f"Process folder '{process_folder}' created!")

        except Exception as e:
            if logger is not None:
                logger.error(f"Error creating process folder '{process_folder}'! Error: {str(e)}")
            pass     


    @staticmethod
    def correct_camera_pixel_per_um(camera_file_name: str, multiplicator:float, logger: RcutilsLogger = None)->bool:
        file_path = VisionProcessClass.get_camera_libary_path(logger) + camera_file_name

        try:
            with open(file_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["camera_params"]
            if "pixelsize" in config:
                config["pixelsize"] *= multiplicator
                FileData["camera_params"] = config

                with open(file_path, "w") as file:
                    yaml.dump(FileData, file)
                
                if logger is not None:
                    logger.info(f"Camera pixel size corrected in {file_path} by a factor of {multiplicator}.")
                return True
            else:
                if logger is not None:
                    logger.error(f"Camera configuration does not contain 'pixelsize' key in {file_path}.")
                return False
            
        except FileNotFoundError:
            if logger is not None:
                logger.error(f"Camera configuration file {file_path} not found!")
            return False
        
        except Exception as e:
            if logger is not None:
                logger.error(f"Error correcting camera pixel size in {file_path}! Error: {str(e)}")
            return False

    @staticmethod
    def correct_camera_angle(camera_file_name: str, angle_diff:float, logger: RcutilsLogger = None)->bool:
        file_path = VisionProcessClass.get_camera_libary_path(logger) + camera_file_name

        try:
            with open(file_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["camera_params"]
            if "camera_axis_1_angle" in config:
                initial_value = config["camera_axis_1_angle"]
                config["camera_axis_1_angle"] += angle_diff
                FileData["camera_params"] = config

                with open(file_path, "w") as file:
                    yaml.dump(FileData, file)
                
                if logger is not None:
                    logger.info(f"Camera angle corrected in {file_path} by factor of {angle_diff}. Initial value was {initial_value}, new value is {config['camera_axis_1_angle']}.")

                return True
            else:
                if logger is not None:
                    logger.error(f"Camera configuration does not contain 'camera_axis_1_angle' key in {file_path}.")
                return False
            
        except FileNotFoundError:
            if logger is not None:
                logger.error(f"Camera configuration file {file_path} not found!")
            return False
        
        except Exception as e:
            if logger is not None:
                logger.error(f"Error correcting camera angle in {file_path}! Error: {str(e)}")
            return False
        
    @staticmethod
    def copy_vision_pipeline_from_file_to_file(source_file_path: str, destination_file_path: str, logger: RcutilsLogger = None) -> bool:
        """
        Copies the vision pipeline from one file to another.
        :param source_file_path: The path to the source file.
        :param destination_file_path: The path to the destination file.
        :param logger: Optional logger for logging messages.
        :return: True if successful, False otherwise.
        """
        try:
            process_library_path = VisionProcessClass.get_process_database_path(logger)
            source_file_path = os.path.join(process_library_path, source_file_path)
            destination_file_path = os.path.join(process_library_path, destination_file_path)
            
            with open(source_file_path, "r") as source_file:
                source_data = json.load(source_file)

            # Extract the vision pipeline
            vision_pipeline = source_data.get("vision_pipeline", [])
            
            # Load existing data from destination file if it exists
            if os.path.exists(destination_file_path):
                with open(destination_file_path, "r") as dest_file:
                    dest_data = json.load(dest_file)
            else:
                dest_data = {}

            # Update the destination data with the vision pipeline
            dest_data["vision_pipeline"] = vision_pipeline

            # Write the updated data back to the destination file
            with open(destination_file_path, "w") as dest_file:
                json.dump(dest_data, dest_file, indent=4)

            if logger is not None:
                logger.info(f"Vision pipeline copied from {source_file_path} to {destination_file_path}.")
            return True

        except Exception as e:
            if logger is not None:
                logger.error(f"Error copying vision pipeline from {source_file_path} to {destination_file_path}! Error: {str(e)}")
            return False

def main(args=None):
    pass

if __name__ == "__main__":
    main()
