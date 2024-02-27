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

class VisionProcessClass:
    """
    Create an ImagePublisher class, which is a subclass of the Node class.
    """

    def __init__(
        self,
        vision_node: Node,
        launch_as_assistant,
        process_filename,
        camera_config_filename,
        db_cross_val_only,
        process_UID,
        image_display_time_visualization,
        open_process_file,
        run_cross_validation,
        show_image_on_error,
        step_through_images,
        ):

        self.br = CvBridge()
        self.vision_node = vision_node
        self.launch_as_assistant = launch_as_assistant
        self.process_filename = process_filename
        self.camera_config_filename = camera_config_filename
        self.process_UID = process_UID
        self.vision_process_id = process_UID
        self.topic_available = False
        self.run_cross_validation = run_cross_validation

        if launch_as_assistant:
            self.show_image_on_error = show_image_on_error
            self.step_through_images = step_through_images
        else:
            self.show_image_on_error = False
            self.step_through_images = False

        self.image_processing_handler = ImageProcessingHandler()
        package_share_directory = get_package_share_directory("pm_vision_manager")
        self.path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"

        
        self.image_display_time_visualization = image_display_time_visualization

        if self.launch_as_assistant:
            self.vision_node.get_logger().info("Starting Vision Assistant!")
            self.image_display_time_visualization = (
                10  # Set the display time in assistant mode
            )
        else:
            self.vision_node.get_logger().info("Execute Vision!")
            if self.image_display_time_visualization < 0:
                self.image_display_time_visualization = 5

        self.vision_node.get_logger().info(
            "Current vision process: " + self.process_filename
        )
        self.vision_node.get_logger().info("Current process ID: " + self.process_UID)
        
        self.process_start_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

        self.process_start_time_ms = self.vision_node.get_clock().now()


        self.show_cross_validation_images = False  # This variable is used for the display of images in cross validation mode

        # self.check_process_file_existence()
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
            # return early if not success
            return

        if open_process_file:
            self.start_vision_app()

        self.counter_error_cross_val = 0
        self.VisionOK_cross_val = True
        #self.VisionOK = False
        self.stop_image_subscription = False
        self.cross_val_failed_images = []
        self.delete_this_object = False
        self.vision_results_path = "None"
        self.results_dict = {}

        if db_cross_val_only: # Hier haben wir ja die Abfahrt Richtung Iterieren der Bilder im Ordner...
            if not launch_as_assistant:
                self.cycle_though_db()
            else:
                self.db_thread = Thread(target=self.cycle_though_db)
                self.db_thread.setDaemon(True)
                self.db_thread.start()
        else:
            self.topic_timer = self.vision_node.create_timer(10, self.image_topic_watchdog, callback_group=vision_node.callback_group)

            self.subscription = vision_node.create_subscription(
                Image,
                self.camera_subscription_topic,  # defined in camera_config.yaml
                self.vision_callback,
                10,
                callback_group=vision_node.callback_group_image_subscriptions)
            self.subscription  # prevent unused variable warning
            vision_node.get_logger().info(f"Subscribing to: '{self.camera_subscription_topic}'. Timeout: 10s")

    def image_topic_watchdog(self):
        if self.topic_available:
            self.topic_available = False
        # if in execute mode
        elif not self.launch_as_assistant:
            self.vision_node.get_logger().error("Timed out! Image topic not available! Exiting...")
            self.delete_this_object = True
            self.vision_node.destroy_subscription(self.subscription)
            self.topic_timer.cancel()
        # if in assistant mode
        elif self.launch_as_assistant and self.stop_image_subscription:
            self.delete_this_object = True
            self.vision_node.destroy_subscription(self.subscription)
            self.topic_timer.cancel()


    def vision_callback(self, data):
        self.topic_available = True
        self.load_assistant_config()
        self.load_process_file()
    

        self.vision_node.get_logger().info("Receiving video frame")
        # Convert ROS Image message to OpenCV image
        received_frame = self.br.imgmsg_to_cv2(data)

        if not self.launch_as_assistant:
            self.stop_image_subscription = True  # in exection mode is this set before the image is processed with the pipeline. This is due to the ability of process_image to set the stop_image_subscription
    
        # run crossvalidation
        if self.run_cross_validation:
            self.execute_crossvalidation()  # Crossvalidation needs to run before the received image is processed, otherwise results dict will contain results from cossvalidation
        
        image_name = self.vision_process_id+"_"+self.process_start_time
        self.image_processing_handler.set_image_metatdata(self.vision_process_id, self.process_db_path, image_name)
        self.image_processing_handler.set_initial_image(received_frame)

        #display_image = process_image(self, received_frame, self.process_pipeline_list)
        display_image, vision_results = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
        self.save_vision_results(self.image_processing_handler.vision_results_dict)

        # Show image
        self.apply_image_for_vizualization(
            self.window_name, display_image, self.image_display_time_visualization
        )

        if self.stop_image_subscription:
            self.vision_node.get_logger().info("Vision Process Ended!")
            self.delete_this_object = True
            self.topic_timer.cancel()
            self.vision_node.destroy_subscription(self.subscription)

    def apply_image_for_vizualization(self, window_name, image, display_time):
        # Check if image is already in image list of node
        found_tuples = [
            (index, item)
            for index, item in enumerate(self.vision_node.image_list)
            if self.window_name == item[0]
        ]

        image_display_start_time = self.vision_node.get_clock().now()

        # if not in image list, add image to image list
        if not found_tuples:
            self.vision_node.image_list.append(
                (window_name, image, display_time, image_display_start_time)
            )

        # if in image list delete it and reappend to list
        else:
            for index, item in found_tuples:
                del self.vision_node.image_list[index]
                self.vision_node.image_list.append(
                    (window_name, image, display_time, image_display_start_time)
                )

    def crossvalidation_keyboard_interrupt(self, key):
        if key == keyboard.Key.space:
            self.next_image = True
            self.show_cross_validation_images = True
            time.sleep(0.75)
            self.vision_node.get_logger().info("SPACE PRESSED!")

    def execute_crossvalidation(self):
        # Starting cross validation with images in folder
        # keyboard_listener.join()

        if self.run_cross_validation and not self.stop_image_subscription:
            self.cross_val_failed_images.clear()
            self.image_processing_handler.cross_val_running = True
            self.counter_error_cross_val = 0
            self.VisionOK_cross_val = True
            self.vision_node.get_logger().info("Starting crossvalidation...")
            try:
                self.next_image = False
                if self.launch_as_assistant and (self.show_image_on_error or self.step_through_images):
                    self.vision_node.get_logger().error("Keyboard listener started! Press 'Space'.")
                    keyboard_listener = keyboard.Listener(on_press=self.crossvalidation_keyboard_interrupt)
                    keyboard_listener.start()

                numb_images_cross_val = len(fnmatch.filter(os.listdir(self.process_db_path), "*.png"))

                print(str(numb_images_cross_val) + " images for crossvalidation")
                for image_in_folder in os.listdir(self.process_db_path):
                    if image_in_folder.endswith(".png"):

                        image = cv2.imread(self.process_db_path + "/" + image_in_folder)
                    
                        print("Processing image: " + image_in_folder)
                        self.load_process_file()
                        self.crossval_image_name = image_in_folder.rstrip(".png")
                        image_name = f"{self.vision_process_id}_{image_in_folder}"
                        
                        self.image_processing_handler.set_image_metatdata(self.vision_process_id, self.process_db_path, image_name)
                        self.image_processing_handler.set_initial_image(image)
                        display_image, _ = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
                        self.save_vision_results(self.image_processing_handler.vision_results_dict)

                        if not self.image_processing_handler.get_vision_ok():
                            self.VisionOK_cross_val = False
                            self.cross_val_failed_images.append(image_in_folder)
                            self.counter_error_cross_val += 1
                                                
                        if (((not self.image_processing_handler.get_vision_ok() and self.show_image_on_error) or self.step_through_images)
                            and self.launch_as_assistant):
                            #and self.show_cross_validation_images
                            self.next_image = False
                            while not self.next_image and not self.stop_image_subscription:
                                self.load_process_file()
                                display_image, _ = process_image(self.vision_node, self.image_processing_handler, self.process_pipeline_list)
                                self.apply_image_for_vizualization(
                                    self.window_name,
                                    display_image,
                                    self.image_display_time_visualization,
                                )
                                time.sleep(0.5)
                if self.counter_error_cross_val == 0:
                    self.vision_node.get_logger().info("Crossvalidation exited with no Error!")

                else:
                    print("Crossvalidation error!")
                    self.vision_node.get_logger().warning(
                        "Crossvalidation had errors! "
                        + str(self.counter_error_cross_val)
                        + "/"
                        + str(numb_images_cross_val)
                        + " images had errors!"
                    )
                print(self.cross_val_failed_images)

                if self.launch_as_assistant and (self.show_image_on_error or self.step_through_images):
                    keyboard_listener.stop()
            except Exception as e:
                self.vision_node.get_logger().error(
                    "No images in DB yet or other error in execution of cross validation!"
                )
                self.vision_node.get_logger().error(str(e))

            self.vision_node.get_logger().info("Crossvalidation ended...")

            self.show_cross_validation_images = (
                False  # reset so that published image is displayed
            )
            self.image_processing_handler.cross_val_running = False

    def load_path_config(self) -> bool:
        try:
            f = open(self.path_config_path)
            FileData = yaml.load(f, Loader=SafeLoader)
            config = FileData["vision_assistant_path_config"]
            self.process_library_path = config["process_library_path"]
            self.vision_database_path = config["vision_database_path"]
            self.camera_config_path = config["camera_config_path"]
            self.vision_assistant_config = config["vision_assistant_config"]
            self.process_file_path = self.process_library_path + self.process_filename
            f.close()
            self.vision_node.get_logger().info("Vision assistant path config loaded!")
            return True
        except:
            self.vision_node.get_logger().error(
                "Error opening vision assistant path configuration: "
                + str(self.path_config_path)
                + "!"
            )
            return False

    def load_assistant_config(self) -> bool:
        try:
            f = open(self.vision_assistant_config)
            FileData = yaml.load(f, Loader=SafeLoader)
            config = FileData["vision_assistant_config"]
            self.show_input_and_output_image = config["show_input_and_output_image"]
            self.scale_ouput_window_to_screen_size = config[
                "scale_ouput_window_to_screen_size"
            ]
            f.close()
            self.vision_node.get_logger().info("Vision assistant config loaded!")
            return True
        except:
            self.vision_node.get_logger().error(
                "Error opening vision assistant configuration: "
                + str(self.vision_assistant_config)
                + "!"
            )
            return False

    def open_process_file_in_vcode(self):
        try:
            Comand = "code " + self.process_file_path
            self.vision_node.get_logger().info(Comand)
            os.system(Comand)
            self.vision_node.get_logger().info("Process File opened!")
        except Exception as e:
            self.vision_node.get_logger().error(e)
            self.vision_node.get_logger().error("Process File could not be opened!")

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
            print(e)

    def set_display_time_for_exit(
        self,
    ):  # this function is used when the vision assistant instance is ended.
        self.image_display_time_visualization = 1

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

            self.init_camera_exposure_time(config=config["exposure_time"])
            self.vision_node.get_logger().info("Camera config loaded!")
            return True
        except Exception as e:
            print(e)
            self.vision_node.get_logger().error(f"Error opening or error in camera config file: {str(self.camera_config_path + self.camera_config_filename)}!")
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

    def create_process_file(self):
        try:
            # default_process_file_metadata_dict = {}
            # default_process_file_metadata_dict["vision_process_name"] = self.process_filename
            # default_process_file_metadata_dict["id_process"] = "default_ID"
            # default_process_file_metadata_dict["File_created"] = str(
            #     datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            # )
            # default_process_file_metadata_dict["vision_pipeline"] = []
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
            f = open(self.process_file_path)
            FileData = json.load(f)
            self.vision_process_name = FileData["vision_process_name"]
            self.process_db_path = self.vision_database_path + self.process_filename.split('.json')[0] # default
            """ Braucht Niklas für seine MA
            self.process_db_path = self.vision_database_path # Einstellen über die config-file
            """
            self.window_name = f"PM Vision Assistant_{self.vision_process_name}_ID: {self.process_UID}"
            f.close()
            self.vision_node.get_logger().info("Process meta data loaded!")
            return True
        except:
            self.vision_node.get_logger().error(
                "Error opening process file: " + str(self.process_file_path) + "!"
            )
            return False

    def load_process_file(self):
        try:
            f = open(self.process_file_path)
            FileData = json.load(f)
            self.process_pipeline_list = FileData["vision_pipeline"]
            f.close()
            self.vision_node.get_logger().info("Process pipeline loaded!")
        except:
            self.vision_node.get_logger().error(
                "Error opening process file: " + str(self.process_file_path) + "!"
            )

    def save_vision_results(self, result_dict):
        result_meta_dict = {}
        
        # Set path for results dict
        if not self.image_processing_handler.cross_val_running:
            vision_results_path = f"{self.process_library_path}{Path(self.process_file_path).stem}_results_{self.camera_id}.json"
            self.vision_results_path = (vision_results_path)  # needed for the service response
        else:
            results_folder_path = f"{self.vision_database_path}{self.process_filename.split('.json')[0]}/{self.camera_id}" # default
            vision_results_path = f"{results_folder_path}/results_{str(self.crossval_image_name)}.json" # default
            """ Braucht Niklas für seine MA
            results_folder_path = f"{self.process_library_path}{self.process_filename.split('Chromosom')[0]}"
            vision_results_path = f"{results_folder_path}/results_{str(self.crossval_image_name)}.json"
            """

            if not os.path.exists(results_folder_path):
                os.makedirs(results_folder_path)
                print("Results folder crossval created!")

        result_meta_dict["vision_process_name"] = self.process_filename
        result_meta_dict["exec_timestamp"] = str(
            datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        )
        result_meta_dict["vision_OK"] = self.image_processing_handler.get_vision_ok()
        result_meta_dict["process_UID"] = self.process_UID
        result_meta_dict["VisionOK_cross_val"] = self.VisionOK_cross_val

        if self.image_processing_handler.cross_val_running:
            result_meta_dict["image_name"] = str(self.crossval_image_name)

        result_meta_dict["failed_images_cross_val"] = self.cross_val_failed_images
        # Insert metadata at the beginning of the dictionary
        result_dict = {**result_meta_dict, **result_dict}

        # used in vision_node
        self.results_dict = result_dict

        try:
            with open(vision_results_path, "w") as outputfile:
                json.dump(result_dict, outputfile,indent=4)
        except:
            self.vision_node.get_logger().warn(f"Vision_results_path: {vision_results_path}")
            self.vision_node.get_logger().error("Error saving vision results!")

    def cycle_though_db(self):
        try:
            if self.launch_as_assistant:
                while (not self.stop_image_subscription):
                    self.execute_crossvalidation()
                self.set_display_time_for_exit()
                self.delete_this_object = True
            else:
                self.execute_crossvalidation()
                self.delete_this_object = True
                
        except KeyboardInterrupt:
            pass

def main(args=None):
    pass

if __name__ == "__main__":
    main()
