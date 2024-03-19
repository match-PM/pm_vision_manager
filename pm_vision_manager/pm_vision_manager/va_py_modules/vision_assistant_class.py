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
import time
from pynput import keyboard
from pathlib import Path
import threading
from rosidl_runtime_py.utilities import get_service #, get_interface, get_message
from pm_vision_manager.va_py_modules.vision_pipline_processing import process_image
from threading import Thread
from rclpy.node import Node
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy, QoSHistoryPolicy, qos_profile_sensor_data
import numpy as np

from PyQt6.QtCore import Qt, QByteArray, pyqtSignal, QObject


SUPPORTED_TYPES = [".png", ".jpg", ".jpeg", ".bmp"]

class CameraExposureTimeError(Exception):
    def __init__(self, message="Camera exposure time service is not available!"):
        self.message = message
        super().__init__(self.message)

def percentage_to_value(percentage, min_value, max_value):
    # Ensure that the percentage is within the valid range (0% to 100%)
    percentage = max(0, min(percentage, 100))
    
    # Convert the percentage to the original value
    value = (percentage / 100) * (max_value - min_value) + min_value
    
    return value

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
        self.topic_available = False

        self.br = CvBridge()
        self.image_processing_handler = ImageProcessingHandler(self.vision_node.get_logger())
        self.image_processing_handler_cross_val = ImageProcessingHandler(self.vision_node.get_logger())
        self.image_processing_handler_cross_val.set_cross_val_running(True)

        package_share_directory = get_package_share_directory("pm_vision_manager")
        self.path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"

        if self.launch_as_assistant:
            self.vision_node.get_logger().info("Starting Vision Assistant!")
        else:
            self.vision_node.get_logger().info("Execute Vision!")


        self.vision_node.get_logger().info(f"Current vision process: {self.process_filename}")
        
        self.process_start_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        self.process_start_time_ms = self.vision_node.get_clock().now()

        path_load_success = self.load_path_config()
        load_config_success = self.load_assistant_config()
        load_meta_success = self.load_process_file_metadata()
        load_camera_success = self.load_camera_config()

        if (
            path_load_success
            and load_config_success
            and load_meta_success
            and load_camera_success
        ):
            self.init_success = True

        else:
            self.vision_node.get_logger().error(f"Initialization of '{self.process_UID} failed!")
            self.init_success = False
            return
        
        self.results_signal = VisionResultsSignal()
        self.set_crossval_results_signal = SetCrossValResultsSignal()

        try:
            self.cross_validation = VisionCrossvalidation(self.process_db_path)
        except Exception as e:
            self.vision_node.get_logger().error(f"Error initializing crossvalidation: {str(e)}")
            self.init_success = False
            return

        self.stop_image_subscription = False
        self.subscription_active = False
        self.delete_this_object = False     # This is only used in assist mode
        self.vision_results_path = "None"
        self.process_pipeline_list: list = []
        self.callback_group = MutuallyExclusiveCallbackGroup()
        self.callback_group_timer = ReentrantCallbackGroup()

    def set_processing_source(self, source:str):
        self.processing_source = source
    
    def image_topic_watchdog(self):
        if self.topic_available:
            self.topic_available = False
        # if in execute mode
        elif not self.launch_as_assistant:
            self.vision_node.get_logger().error("Timed out! Image topic not available! Exiting...")
            self.stop_image_subscription = True
            self.delete_this_object = True
            # This is needed for the response(success) of the service call
            self.image_processing_handler.set_vision_ok(False)
            self.vision_node.destroy_subscription(self.subscription)
            self.topic_timer.cancel()

    def start_vision_subscription(self):
        self.subscription_active = True
        self.subscription = self.vision_node.create_subscription(
            Image,
            self.camera_subscription_topic,  # defined in camera_config.yaml
            self.topic_cbk,
            qos_profile=qos_profile_sensor_data,
            callback_group=self.callback_group)
        self.subscription
        if not self.launch_as_assistant:
            self.vision_node.get_logger().info("Starting watchdog for image topic with timeout of 10s...")
            self.topic_timer = self.vision_node.create_timer(10, self.image_topic_watchdog, callback_group=self.callback_group_timer)

    def stop_vision_subscription(self) -> bool:
        if self.subscription_active:
            self.vision_node.destroy_subscription(self.subscription)
            if not self.launch_as_assistant:
                self.topic_timer.cancel()
            self.subscription_active = False
            return True

    def topic_cbk(self, data):
        self.subscription_active = True
        self.topic_available = True
        self.stop_image_subscription = True
        self.load_process_file()

        self.vision_node.get_logger().info("Receiving video frame")
        # Convert ROS Image message to OpenCV image
        received_frame = self.br.imgmsg_to_cv2(data)

        if self.launch_as_assistant:
            image_name = f"{self.process_UID}"
        else:
            image_name = f"{self.process_UID}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"

        self.image_processing_handler.set_image_metatdata(self.process_db_path,image_name)
        self.image_processing_handler.set_initial_image(received_frame)

        #display_image = process_image(self, received_frame, self.process_pipeline_list)
        display_image, vision_results = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
        final_image = self.image_processing_handler.get_final_image()
        _results = self.save_vision_results(self.image_processing_handler.get_results())
        self.results_signal.signal.emit(final_image, _results)

        # this only runs in execution mode and when the execution is finished
        if not self.launch_as_assistant and self.stop_image_subscription:   # self.stop_image_subscription may be overwritten in process_image function
            if self.run_cross_validation:
                self.execute_crossvalidation()
                # reinitilize the results after crossvalidation has been executed
                _results = self.save_vision_results(self.image_processing_handler.get_results())
                self.results_signal.signal.emit(final_image, _results)
            self.stop_vision_subscription()

    def vision_assistant_loop(self):
        _current_source = self.processing_source

        while not self.delete_this_object:

            if self.processing_source is None:
                self.vision_node.get_logger().debug("No image source selected!")
                time.sleep(0.5)
                continue

            elif self.processing_source == self.camera_subscription_topic and _current_source != self.camera_subscription_topic:
                _current_source = self.camera_subscription_topic
                self.start_vision_subscription()
                self.vision_node.get_logger().info("Camera subscription started!")
                continue

            elif self.processing_source == self.camera_subscription_topic and _current_source == self.camera_subscription_topic:
                time.sleep(0.5)
                continue
                
            # At this point image must be an image from crossvalidation
            elif _current_source != self.processing_source:
                if self.subscription_active:
                    self.stop_vision_subscription()
                _current_source = self.processing_source
                db_image = self.cross_validation.get_image_by_filename(self.processing_source)
                
            elif  self.processing_source == _current_source:
                pass

            # This case should never happen
            else:
                self.vision_node.get_logger().warn("Strange behaviour detected. Contact maintainer")
                time.sleep(0.5)
                continue
            
            self.process_image_for_widget(db_image, os.path.splitext(self.processing_source)[0])
            
            time.sleep(0.5)
        
        if self.subscription_active:
            self.stop_vision_subscription()

    def exit_class(self):
        self.vision_node.get_logger().debug("VA: Exiting Vision Process!")
        self.delete_this_object = True

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

        self.load_process_file()

        for index, current_image_file in enumerate(self.cross_validation.images):
            
            # Set the filename without the extension
            self.cross_validation.current_image_name = os.path.splitext(current_image_file)[0]

            image = self.cross_validation.get_image_by_filename(current_image_file)    
            
            image_name = f"{self.cross_validation.current_image_name}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"
            self.image_processing_handler_cross_val.set_image_metatdata(self.process_db_path, image_name)
            self.image_processing_handler_cross_val.set_initial_image(image)
            display_image, _ = process_image(self.vision_node, self.image_processing_handler_cross_val, self.process_pipeline_list)
            
            self.save_vision_results(self.image_processing_handler_cross_val.get_results())

            if not self.image_processing_handler_cross_val.get_vision_ok():
                self.cross_validation.visionOK = False
                self.cross_validation.append_to_failed_images(current_image_file)
                self.cross_validation.counter_error += 1
        
        self.cross_validation.has_been_executed = True
        # this signal is only used in execution mode. In assistant mode the signal has no effect
        self.set_crossval_results_signal.signal.emit(self.cross_validation.get_failed_images())
        self.vision_node.get_logger().info("Crossvalidation ended...")
        self.cross_validation.stop_cross_val()

    def process_image_for_widget(self, image:np.ndarray, image_name:str=""):
        self.load_process_file()
        self.image_processing_handler.set_initial_image(image)
        self.image_processing_handler.set_image_metatdata(self.process_db_path, image_name)
        display_image, _ = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
        _results = self.save_vision_results(self.image_processing_handler.get_results())
        self.results_signal.signal.emit(self.image_processing_handler.get_final_image(), _results)
    

    def load_path_config(self) -> bool:
        try:
            with open(self.path_config_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["vision_assistant_path_config"]
            self.process_library_path = config["process_library_path"]
            self.vision_database_path = config["vision_database_path"]
            self.camera_config_path = config["camera_config_path"]
            self.vision_assistant_config = config["vision_assistant_config"]
            self.process_file_path = self.process_library_path + self.process_filename
            self.vision_node.get_logger().info("Vision assistant path config loaded!")
            return True
        except Exception as e:
            self.vision_node.get_logger().error(f"Error opening vision assistant path configuration: '{str(self.path_config_path)}'! Error: {str(e)}")
            return False

    def load_assistant_config(self) -> bool:
        try:
            with open(self.vision_assistant_config, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["vision_assistant_config"]
            self.show_input_and_output_image = config["show_input_and_output_image"]
            self.scale_ouput_window_to_screen_size = config["scale_ouput_window_to_screen_size"]
            self.vision_node.get_logger().info("Vision assistant config loaded!")
            return True
        except Exception as e:
            self.vision_node.get_logger().error(f"Error opening vision assistant configuration: '{str(self.vision_assistant_config)}'! Error: {str(e)}!")
            return False

    def start_vision_app(self):
        try:
            app_thread = threading.Thread(target=self.open_process_file_in_app)
            app_thread.start()
            
        except Exception as e:
            self.vision_node.get_logger().error(e)
            self.vision_node.get_logger().error("Process File could not be opened!")

    def open_process_file_in_app(self):
        try:
            arguments = [f"pipeline_file_path:{self.process_file_path}"]
            python_file_path = f"{get_package_prefix('pm_vision_app')}/lib/python3.10/site-packages/pm_vision_app/vision_assistant_app.py"
            command = ['python3', python_file_path] + arguments
            subprocess.run(command)
            
        except Exception as e:
            self.vision_node.get_logger().error(e)
            self.vision_node.get_logger().error("Process File could not be opened!")

    @staticmethod
    def check_for_valid_inputs(process_file_name:str, camera_file_name:str, logger = None)->bool:
        
        if process_file_name is None or camera_file_name is None:
            return False
        
        package_share_directory = get_package_share_directory("pm_vision_manager")
        path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
        try:
            with open(path_config_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["vision_assistant_path_config"]
            process_library_path = config["process_library_path"]
            camera_config_path = config["camera_config_path"]
            process_file_path = process_library_path + process_file_name
            camera_file_path = camera_config_path + camera_file_name
            if os.path.exists(process_file_path) and os.path.exists(camera_file_path):
                return True
            else:
                return False
        except KeyError as e:
            if logger is not None:  
                logger.error(f"Error in path config file: {str(e)}")
            return False
        except FileNotFoundError as e:
            if logger is not None:
                logger.error(f"Error opening path config file: {str(e)}")
            return False
    
    @staticmethod
    def check_for_valid_path_config(logger=None)->bool:
        package_share_directory = get_package_share_directory("pm_vision_manager")
        path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
        try:
            with open(path_config_path, "r") as file:
                FileData = yaml.safe_load(file)

            config = FileData["vision_assistant_path_config"]
            process_library_path = config["process_library_path"]
            camera_config_path = config["camera_config_path"]
            vision_database_path = config["vision_database_path"]
            if os.path.exists(process_library_path) and os.path.exists(camera_config_path) and os.path.exists(vision_database_path):
                return True
            else:
                if logger is not None:
                    logger.error("Path config file is not valid!")
                return False
        except KeyError as e:
            if logger is not None:
                logger.error(f"Error in path config file: {str(e)}")
            return False
        except FileNotFoundError as e:
            if logger is not None:
                logger.error(f"Error opening path config file: {str(e)}")


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

            self.init_camera_exposure_time(config=config["exposure_time"])
            self.vision_node.get_logger().info("Camera config loaded!")
            return True
        except Exception as e:
            self.vision_node.get_logger().error(f"Error opening or error in camera config file: {str(self.camera_config_path + self.camera_config_filename)}! Error: {str(e)}")
            return False
        
    def init_camera_exposure_time(self, config:dict):
        # Instanciating Exposure Time interface from yaml
        try:
            self.image_processing_handler.srv_client_exposure_time = config["srv_client_name"]
            self.image_processing_handler.srv_type_exposure_time = config["srv_type"]
            self.image_processing_handler.min_val_exposure_time = config["min_val"]
            self.image_processing_handler.max_val_exposure_time = config["max_val"]

            service_metaclass = get_service(self.image_processing_handler.srv_type_exposure_time)

            self.image_processing_handler.client_exposure_time = self.vision_node.create_client(service_metaclass, self.image_processing_handler.srv_client_exposure_time)

            if not self.image_processing_handler.client_exposure_time.wait_for_service(timeout_sec=1.0):
                self.vision_node.get_logger().warn("Exposure time client not online!")
                raise CameraExposureTimeError

            self.image_processing_handler.exposure_time_interface_available = True
            self.image_processing_handler.set_camera_exposure_time = self.set_camera_exposure_time

        except KeyError as e:
            self.vision_node.get_logger().warn(f"Error in camera exposure_time config or not defined!")

        except ValueError as e:
            self.vision_node.get_logger().warn(f"Service interface '{self.image_processing_handler.srv_type_exposure_time}' not installed!")

        except CameraExposureTimeError as e:
            self.vision_node.get_logger().warn(str(e))
        
        except Exception as e:
            self.vision_node.get_logger().error(str(type(e).__name__))
            self.vision_node.get_logger().error(str(e))

        finally:
            if not self.image_processing_handler.exposure_time_interface_available:
                self.vision_node.get_logger().warn("Camera exposure time interface not available!")
            else:
                self.vision_node.get_logger().info("Camera exposure time interface is available!")

    def set_camera_exposure_time(self, exposure_value_percent):
        if self.image_processing_handler.exposure_time_interface_available:
            # Convert the percentage to a actual exposue time value
            exposure_time = percentage_to_value(exposure_value_percent,
                                    self.image_processing_handler.min_val_exposure_time,
                                    self.image_processing_handler.max_val_exposure_time)
            
            # Only if is an valid value (This should normaly be the case, but I the config is wrong it might not)
            if (exposure_time <= self.image_processing_handler.max_val_exposure_time) and (
                exposure_time >= self.image_processing_handler.min_val_exposure_time):
                
                if self.image_processing_handler.camera_exposure_time_set_value != exposure_value_percent:
                    service_request = get_service(self.image_processing_handler.srv_type_exposure_time).Request()
                    value_key = None
                    for _key, _value in service_request.get_fields_and_field_types().items():
                        if _value == 'double' or _value == 'float':
                            value_key = _key
                    if value_key is None:
                        self.vision_node.get_logger().error(f"No field of type 'double' found in service request of type '{self.image_processing_handler.srv_type_exposure_time}'.")
                        return False
                    setattr(service_request, value_key, exposure_time)
                    if not self.image_processing_handler.client_exposure_time.wait_for_service(timeout_sec=1.0):
                        self.vision_node.get_logger().error("Camera exposure service not available!")
                    response = self.image_processing_handler.client_exposure_time.call(service_request)

                    self.image_processing_handler.camera_exposure_time_set_value = exposure_value_percent
                    self.vision_node.get_logger().info(f"Camera exposure time set to '{exposure_time}'!")
                    # This needs to be set so that in 'Execute Vision' the callback gets another image with the new exposure time
                    self.stop_image_subscription = False
                    return True
            else:
                self.vision_node.get_logger().error("Camera exposure time not set! Invalid bounds!")
        else:
            self.vision_node.get_logger().warn("Camera exposure time not available!")
            return False
        
    def check_process_file_existence(self):
        if os.path.exists(self.process_file_path) == False:
            self.vision_node.get_logger().warning("Given Process File does not exist!")
            if self.launch_as_assistant:
                print(f"Should {self.process_file_path} be created?")
                print("Enter y/n to continue")
                while True:
                    a = input()
                    if a == "y":
                        self.create_process_file()
                        break
                    elif a == "n":
                        print("Process File will not be created!")
                        break
                    elif a == "exit":
                        print("Process File will not be created!")
                        break
                    else:
                        print("Enter either yes/no")
                            
    def get_crossval_image_info(self)->tuple[int, int]:
        """
        Returns the current image count and the total number of images in the cross validation folder
        :return: current_image_count, numb_images_cross_val
        :rtype: int, int
        """
        return self.cross_validation.current_image_index, self.cross_validation.get_total_number_images()
    
    def create_process_file(self):
        try:
            default_process_file_metadata_dict = self.create_default_process_dict(self.process_filename)
            # Create folders if not existend
            Path(os.path.dirname(self.process_file_path)).mkdir(
                parents=True, exist_ok=True
            )
            with open(self.process_file_path, "w+") as outputfile:
                json.dump(default_process_file_metadata_dict, outputfile,indent=4)
        except Exception as e:
            print(e)
            self.vision_node.get_logger().error("Error creating process file")
    
    @staticmethod
    def create_default_process_dict(process_name):
        default_process_file_metadata_dict = {}
        default_process_file_metadata_dict["vision_process_name"] = process_name
        default_process_file_metadata_dict["id_process"] = "default_ID"
        default_process_file_metadata_dict["File_created"] = str(
            datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        )
        default_process_file_metadata_dict["vision_pipeline"] = []
        return default_process_file_metadata_dict
    
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

    def load_process_file(self):
        try:
            with open(self.process_file_path, "r") as file:
                FileData = json.load(file)
            self.process_pipeline_list.clear()
            self.process_pipeline_list = FileData["vision_pipeline"]
            self.vision_node.get_logger().info("Process pipeline loaded!")
        except Exception as e:
            self.vision_node.get_logger().error(
                f"Error opening process file: {str(self.process_file_path)}! Error: {str(e)}"
            )

    def save_vision_results(self, result_dict:dict)->dict:
        """
        The function add metadata to the results dict and saves it to a json file
        :param result_dict: The results of the vision process
        :type result_dict: dict
        :return: The results of the vision process
        :rtype: dict
        """
        result_dict = self.construct_results_metadata(result_dict)
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

            if not os.path.exists(results_folder_path):
                os.makedirs(results_folder_path)
                print("Results folder crossval created!")

        try:
            with open(vision_results_path, "w") as outputfile:
                json.dump(result_dict, outputfile,indent=4)
        except:
            self.vision_node.get_logger().warn(f"Vision_results_path: {vision_results_path}")
            self.vision_node.get_logger().error("Error saving vision results!")

        return result_dict

    def construct_results_metadata(self, result_dict:dict)->dict:
        result_meta_dict = {}

        result_meta_dict["vision_process_name"] = self.process_filename
        result_meta_dict["exec_timestamp"] = str(
            datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        )
        result_meta_dict["vision_OK"] = self.image_processing_handler.get_vision_ok()
        result_meta_dict["process_UID"] = self.process_UID

        if self.cross_validation.check_cross_val_running():
            result_meta_dict["image_name"] = str(self.cross_validation.current_image_name)

        if self.cross_validation.has_been_executed and not self.cross_validation.check_cross_val_running():
            result_meta_dict["VisionOK_cross_val"] = self.cross_validation.visionOK
            result_meta_dict["failed_images_cross_val"] = self.cross_validation.failed_images
            result_meta_dict["total_images_cross_val"] = self.cross_validation.numb_images
            result_meta_dict["failed_images_count"] = self.cross_validation.counter_error

        # Insert metadata at the beginning of the dictionary
        result_dict = {**result_meta_dict, **result_dict}

        return result_dict

def main(args=None):
    pass

if __name__ == "__main__":
    main()
