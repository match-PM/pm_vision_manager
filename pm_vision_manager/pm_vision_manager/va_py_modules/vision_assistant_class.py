# Import the necessary libraries
from sensor_msgs.msg import Image  # Image is the message type
import cv2  # OpenCV library
import json
import numpy as np
import os
from os import listdir
from datetime import datetime
import yaml
import fnmatch
from yaml.loader import SafeLoader
import subprocess
from ament_index_python.packages import get_package_share_directory, get_package_prefix
import math
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
from math import pi
import time
from pynput import keyboard
from pathlib import Path
import sys
import threading
from functools import partial
from pm_vision_manager.va_py_modules.vision_processes import process_image
from pm_vision_manager.va_py_modules.vision_utils import (
    image_resize,
    degrees_to_rads,
    rads_to_degrees,
    get_screen_resolution,
    rotate_image,
)
from pm_vision_interfaces.srv import ExecuteVision
from rclpy.node import Node


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
        """
        Class constructor to set up the node
        """
        self.br = CvBridge()
        self.vision_node = vision_node
        self.process_UID = process_UID
        self.process_filename = process_filename
        self.camera_config_filename = camera_config_filename
        package_share_directory = get_package_share_directory("pm_vision_manager")
        self.path_config_path = (
            package_share_directory + "/vision_assistant_path_config.yaml"
        )
        self.vision_process_id = process_UID
        self.launch_as_assistant = launch_as_assistant
        self.image_display_time_visualization = image_display_time_visualization

        if self.launch_as_assistant:
            self.vision_node.get_logger().info("Starting node in assistant mode!")
            self.image_display_time_visualization = (
                10  # Set the display time in assistant mode
            )
        else:
            self.vision_node.get_logger().info("Starting node in processing mode!")
            if self.image_display_time_visualization < 0:
                self.image_display_time_visualization = 5

        self.vision_node.get_logger().info(
            "Current vision process: " + self.process_filename
        )
        self.vision_node.get_logger().info("Current process ID: " + self.process_UID)
        self.run_cross_validation = run_cross_validation
        timestamp = datetime.now()
        self.screen_resolution = get_screen_resolution()
        self.screen_height = int(self.screen_resolution["height"].decode("UTF-8"))
        self.screen_width = int(self.screen_resolution["width"].decode("UTF-8"))
        self.vision_node.get_logger().info(
            "Screen resolution: "
            + str(self.screen_width)
            + "x"
            + str(self.screen_height)
        )
        self.process_start_time = timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        # Used to convert between ROS and OpenCV images

        self.process_start_time_ms = self.vision_node.get_clock().now()

        self.show_image_on_error = False
        self.step_through_images = False
        self.show_cross_validation_images = False  # This variable is used for the display of images in cross validation mode

        if launch_as_assistant:
            self.show_image_on_error = show_image_on_error
            self.step_through_images = step_through_images

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
        self.cross_val_running = False
        self.VisionOK = False
        self.stop_image_subscription = False
        self.results_dict = {}
        self.cross_val_failed_images = []
        self.delete_this_object = False
        self.vision_results_path = "None"

        if db_cross_val_only:
            self.cycle_though_db()

        else:
            self.subscription = vision_node.create_subscription(
                Image,
                self.camera_subscription_topic,  # defined in camera_config.yaml
                self.Vision_callback,
                10,
                callback_group=vision_node.callback_group_image_subscriptions,
            )
            self.subscription  # prevent unused variable warning
            vision_node.get_logger().info(
                "Subscribing to: " + self.camera_subscription_topic
            )

    def Vision_callback(self, data):
        self.load_assistant_config()
        self.load_process_file()
        self.window_name = (
            "PM Vision Assistant"
            + "_"
            + self.vision_process_name
            + "ID: "
            + self.process_UID
        )

        self.vision_node.get_logger().info("Receiving video frame")
        # Convert ROS Image message to OpenCV image
        received_frame = self.br.imgmsg_to_cv2(data)

        if not self.launch_as_assistant:
            self.stop_image_subscription = True  # in exection mode is this set before the image is processed with the pipeline. This is due to the ability of process_image to set the stop_image_subscription

        # run crossvalidation
        if self.run_cross_validation:
            self.execute_crossvalidation()  # Cossvalidation needs to run before the received image is processed, otherwise results dict will contain results from cossvalidation

        display_image = process_image(self, received_frame, self.process_pipeline_list)

        # Show image
        self.apply_image_for_vizualization(
            self.window_name, display_image, self.image_display_time_visualization
        )

        if self.stop_image_subscription:
            self.vision_node.get_logger().info("Vision Process Ended!")
            self.delete_this_object = True
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

        if self.run_cross_validation:
            self.cross_val_failed_images.clear()
            self.cross_val_running = True
            self.counter_error_cross_val = 0
            self.VisionOK_cross_val = True
            self.vision_node.get_logger().info("Starting crossvalidation...")
            try:
                self.next_image = False
                if self.launch_as_assistant and (
                    self.show_image_on_error or self.step_through_images
                ):
                    keyboard_listener = keyboard.Listener(
                        on_press=self.crossvalidation_keyboard_interrupt
                    )
                    keyboard_listener.start()
                # Get number of images to be processed
                numb_images_cross_val = len(
                    fnmatch.filter(os.listdir(self.process_db_path), "*.png")
                )
                print(str(numb_images_cross_val) + " images for crossvalidation")
                for image_in_folder in os.listdir(self.process_db_path):
                    if image_in_folder.endswith(".png"):
                        image = cv2.imread(self.process_db_path + "/" + image_in_folder)
                        print("----------------------------")
                        print("Processing image: " + image_in_folder)
                        # Calculate VisionOK on image
                        self.load_process_file()
                        self.crossval_image_name = image_in_folder
                        display_image = process_image(
                            self, image, self.process_pipeline_list
                        )

                        if not self.VisionOK:
                            self.VisionOK_cross_val = False
                            self.cross_val_failed_images.append(image_in_folder)

                        # Display image if in assist mode and (step_though images or an error accured)
                        print(self.launch_as_assistant)
                        print(self.VisionOK)
                        print(self.show_image_on_error)
                        print(self.step_through_images)
                        if (
                            (
                                (not self.VisionOK and self.show_image_on_error)
                                or self.step_through_images
                            )
                            and self.launch_as_assistant
                            and self.show_cross_validation_images
                        ):
                            self.next_image = False
                            while not self.next_image:
                                self.load_process_file()
                                display_image = process_image(
                                    self, image, self.process_pipeline_list
                                )
                                self.apply_image_for_vizualization(
                                    self.window_name,
                                    display_image,
                                    self.image_display_time_visualization,
                                )
                                time.sleep(0.5)

                if self.counter_error_cross_val == 0:
                    self.vision_node.get_logger().info(
                        "Crossvalidation exited with no Error!"
                    )

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

                if self.launch_as_assistant and (
                    self.show_image_on_error or self.step_through_images
                ):
                    keyboard_listener.stop()
            except:
                self.vision_node.get_logger().error(
                    "No images in DB yet or other error in execution of cross validation!"
                )

            self.vision_node.get_logger().info("Crossvalidation ended...")

            self.show_cross_validation_images = (
                False  # reset so that published image is displayed
            )
            self.cross_val_running = False

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
            f = open(self.camera_config_path + self.camera_config_filename)
            FileData = yaml.load(f, Loader=SafeLoader)
            config = FileData["camera_params"]
            self.pixelsize = config["pixelsize"]
            self.camera_id = config["cameraname"]
            self.magnification = config["magnification"]
            self.camera_axis_1 = config["camera_axis_1"]
            self.camera_axis_2 = config["camera_axis_2"]
            self.camera_axis_1_angle = config["camera_axis_1_angle"]
            self.camera_axis_2_angle = config["camera_axis_2_angle"]
            self.camera_subscription_topic = config["subscription_topic"]
            self.exposure_time_interface_available = False

            # Instanciating Exposure Time interface from yaml
            try:
                from pylon_ros2_camera_interfaces.srv import SetExposure

                if config["exposure_time"]["channel"] == "service":
                    print(config["exposure_time"]["name"])
                    service_name = str(config["exposure_time"]["name"])
                    self.camera_exposure_time_srv = self.vision_node.create_client(
                        SetExposure, service_name
                    )
                    if not self.camera_exposure_time_srv.wait_for_service(
                        timeout_sec=2.0
                    ):
                        raise Exception("Exposure Time Service not available!")
                    self.camera_exposure_time_type = config["exposure_time"]["type"]
                    self.camera_exposure_time_min_val = config["exposure_time"][
                        "min_val"
                    ]
                    self.camera_exposure_time_max_val = config["exposure_time"][
                        "max_val"
                    ]
                    self.camera_exposure_time_set_value = None
                    self.exposure_time_interface_available = True
            except Exception as e:
                self.vision_node.get_logger().error(str(e))
                self.vision_node.get_logger().warn(
                    "Error in configuring camera or no exposure time interface available!"
                )

            # Calculate Camera parameter
            self.pixelPROum = self.magnification / self.pixelsize
            self.umPROpixel = self.pixelsize / self.magnification
            f.close()
            self.vision_node.get_logger().info("Camera config loaded!")
            return True
        except Exception as e:
            print(e)
            self.vision_node.get_logger().error(
                "Error opening camera config file: "
                + str(self.camera_config_path + self.camera_config_filename)
                + "!"
            )
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
            default_process_file_metadata_dict = {}
            default_process_file_metadata_dict["vision_process_name"] = self.pro
            default_process_file_metadata_dict["id_process"] = "default_ID"
            default_process_file_metadata_dict["File_created"] = str(
                datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            )
            default_process_file_metadata_dict["vision_pipeline"] = []
            # Create folders if not existend
            Path(os.path.dirname(self.process_file_path)).mkdir(
                parents=True, exist_ok=True
            )
            with open(self.process_file_path, "w+") as outputfile:
                json.dump(default_process_file_metadata_dict, outputfile)
        except Exception as e:
            print(e)
            self.vision_node.get_logger().error("Error creating process file")

    def set_camera_exposure_time(self, exposure_value):
        if self.exposure_time_interface_available:
            if (exposure_value < self.camera_exposure_time_max_val) and (
                exposure_value > self.camera_exposure_time_min_val
            ):
                if self.camera_exposure_time_set_value != exposure_value:
                    client_test = self.camera_exposure_time_srv
                    print(exposure_value)
                    print(self.camera_exposure_time_max_val)
                    print(self.camera_exposure_time_min_val)
                    self.vision_node.get_logger().error("CHANGGGEE DETEECCTED")
                    setting_request = SetExposure.Request()
                    print(setting_request.get_fields_and_field_types())

                    if self.camera_exposure_time_type == "float":
                        setting_request.target_exposure = float(exposure_value)
                    elif self.camera_exposure_time_type == "int":
                        setting_request.target_exposure = int(exposure_value)

                    if not client_test.wait_for_service(timeout_sec=2.0):
                        self.vision_node.get_logger().error(
                            "Spawn Service not available"
                        )

                    future = client_test.call_async(setting_request)
                    future.add_done_callback(partial(self.callback_set))

                    # self.future.result()
                    self.camera_exposure_time_set_value = exposure_value
                    self.vision_node.get_logger().info("Service call!!!!")
                    # response.success = True
                    return True
            else:
                self.vision_node.get_logger().error(
                    "Camera exposure time not set! Invalid bounds!"
                )
        else:
            self.vision_node.get_logger().warn("Camera exposure time not available!")
            return False

    def callback_set(self, future):
        try:
            response = future.result()
            self.vision_node.get_logger().info("Exposure Time Set")
        except Exception as e:
            self.vision_node.get_logger().error("error")

    def load_process_file_metadata(self) -> bool:
        try:
            f = open(self.process_file_path)
            FileData = json.load(f)
            self.vision_process_name = FileData["vision_process_name"]
            # self.vision_process_id=FileData['id_process']
            self.process_db_path = self.vision_database_path + self.vision_process_name
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
        if not self.cross_val_running:
            vision_results_path = (
                self.process_library_path
                + Path(self.process_file_path).stem
                + "_results_"
                + self.camera_id
                + ".json"
            )
            self.vision_results_path = (
                vision_results_path  # needed for the service response
            )
        else:
            results_folder_path = f"{self.vision_database_path}/{Path(self.process_file_path).stem}_{self.camera_id}"
            vision_results_path = (
                results_folder_path
                + "/"
                + "results_"
                + str(self.crossval_image_name)
                + ".json"
            )

            if not os.path.exists(results_folder_path):
                os.makedirs(results_folder_path)
                print("Results folder crossval created!")

        result_meta_dict["vision_process_name"] = self.process_filename
        result_meta_dict["exec_timestamp"] = str(
            datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        )
        result_meta_dict["vision_OK"] = self.VisionOK
        result_meta_dict["process_UID"] = self.process_UID
        result_meta_dict["VisionOK_cross_val"] = self.VisionOK_cross_val

        if self.cross_val_running:
            result_meta_dict["image_name"] = str(self.crossval_image_name)
        result_meta_dict["failed_images_cross_val"] = self.cross_val_failed_images
        # Insert metadata at the beginning of the dictionary
        result_dict = {**result_meta_dict, **result_dict}

        self.results_dict = result_dict

        try:
            with open(vision_results_path, "w") as outputfile:
                json.dump(result_dict, outputfile)
        except:
            self.vision_node.get_logger().error("Error saving vision results!")

    def create_vision_element_overlay(self, displ_frame, vis_elem_frame):
        # Add visual elements to the display frame
        if len(displ_frame.shape) < 3:
            displ_frame = cv2.cvtColor(displ_frame, cv2.COLOR_GRAY2BGR)
        # Now create a mask of logo and create its inverse mask also
        mask_frame = cv2.cvtColor(vis_elem_frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask_frame, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(displ_frame, displ_frame, mask=mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(vis_elem_frame, vis_elem_frame, mask=mask)
        # Put logo in ROI and modify the main image
        displ_frame = cv2.add(img1_bg, img2_fg)
        return displ_frame

    def CS_Conv_ROI_Pix_TO_Img_Pix(self, x_roi, y_roi):
        if self.ROI_used:
            x_img = self.ROI_CS_CV_top_left_x + x_roi
            y_img = self.ROI_CS_CV_top_left_y + y_roi
        else:
            x_img = x_roi
            y_img = y_roi
        return x_img, y_img

    def CS_Conv_Pixel_Top_Left_TO_Center(self, img_width, img_height, x_tl, y_tl):
        x_center = int(round(x_tl - img_width / 2))
        y_center = int(round(img_height / 2 - y_tl))
        return x_center, y_center

    def CS_Conv_Pixel_Center_TO_Top_Left(
        self, img_width, img_height, x_center, y_center
    ):
        x_tl = int(round(img_width / 2) + x_center)
        y_tl = int(round(img_height / 2) - y_center)
        return x_tl, y_tl

    def adaptImagewithROI(self, disp_frame, prcs_frame):
        if self.ROI_used:
            x_offset = self.ROI_CS_CV_top_left_x
            y_offset = self.ROI_CS_CV_top_left_y
            disp_frame[
                y_offset : y_offset + prcs_frame.shape[0],
                x_offset : x_offset + prcs_frame.shape[1],
            ] = prcs_frame
        else:
            disp_frame = prcs_frame
        return disp_frame

    def CS_Camera_TO_Image(self, x_val_c, y_val_c):
        if self.camera_axis_2_angle == "-":
            y_val_c = -y_val_c
        x_val_i = x_val_c * math.cos(
            2 * pi - degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_c * math.sin(2 * pi - degrees_to_rads(self.camera_axis_1_angle))
        y_val_i = -x_val_c * math.sin(
            2 * pi - degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_c * math.cos(2 * pi - degrees_to_rads(self.camera_axis_1_angle))
        return x_val_i, y_val_i

    def CS_Image_TO_Camera(self, x_val_i, y_val_i):
        x_val_c = x_val_i * math.cos(
            degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_i * math.sin(degrees_to_rads(self.camera_axis_1_angle))
        y_val_c = -x_val_i * math.sin(
            degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_i * math.cos(degrees_to_rads(self.camera_axis_1_angle))
        if self.camera_axis_2_angle == "-":
            y_val_c = -y_val_c
        return x_val_c, y_val_c

    def CS_Image_TO_Pixel(self, x_val_i, y_val_i):
        x_val_pix = int(round(self.pixelPROum * x_val_i))
        y_val_pix = int(round(self.pixelPROum * y_val_i))
        return x_val_pix, y_val_pix

    def CS_Pixel_TO_Image(self, x_val_pix, y_val_pix):
        x_val_i = x_val_pix * self.umPROpixel
        y_val_i = y_val_pix * self.umPROpixel
        return x_val_i, y_val_i

    def CS_CV_TO_camera_with_ROI(self, x_ROI, y_ROI):
        x_tl, y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(x_ROI, y_ROI)
        x_center_pix, y_center_pix = self.CS_Conv_Pixel_Top_Left_TO_Center(
            self.img_width, self.img_height, x_tl, y_tl
        )
        x_center_image_um, y_center_image_um = self.CS_Pixel_TO_Image(
            x_center_pix, y_center_pix
        )
        x_cs_camera, y_cs_camera = self.CS_Image_TO_Camera(
            x_center_image_um, y_center_image_um
        )
        return x_cs_camera, y_cs_camera

    def cycle_though_db(self):
        try:
            while True:
                self.run_cross_validation()
        except KeyboardInterrupt:
            pass

    # def process_image(self,received_frame,_process_pipeline_list):

    #   self.img_width  = received_frame.shape[1]
    #   self.img_height = received_frame.shape[0]
    #   self.FOV_width=self.umPROpixel*self.img_width
    #   self.FOV_height=self.umPROpixel*self.img_height
    #   self.ROI_used=False
    #   print("FOV width is " + str(self.FOV_width) + "um")
    #   print("FOV hight is " + str(self.FOV_height) + "um")
    #   frame_buffer=[]
    #   frame_processed = received_frame
    #   frame_visual_elements = np.zeros((received_frame.shape[0], received_frame.shape[1], 3), dtype = np.uint8)
    #   display_frame=received_frame
    #   frame_buffer.append(received_frame)
    #   self.VisionOK = True
    #   vision_results_file_dict={}
    #   vision_results_list=[]
    #   try:
    #     pipeline_list=_process_pipeline_list
    #     for list_item in pipeline_list:
    #     # Iterating through the json
    #       for key, function_parameter in list_item.items():
    #         match key:
    #           case "threshold":
    #               active = function_parameter['active']
    #               thresh = function_parameter['thresh']
    #               maxval = function_parameter['maxval']
    #               type = function_parameter['type']
    #               if active:
    #                   _Command = "cv2." + type
    #                   _,frame_processed = cv2.threshold(frame_processed,thresh,maxval,exec(_Command))
    #                   print("Theshold executed")
    #                   display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                   frame_buffer.append(frame_processed)
    #           case "adaptiveThreshold":
    #               active = function_parameter['active']
    #               maxValue = function_parameter['maxValue']
    #               adaptiveMethod = function_parameter['adaptiveMethod']
    #               thresholdType = function_parameter['thresholdType']
    #               blockSize = function_parameter['blockSize']
    #               C_Value = function_parameter['C']
    #               if active:
    #                   _Command_adaptiveMethod = "cv2." + adaptiveMethod
    #                   _Command_thresholdType = "cv2." + thresholdType
    #                   frame_processed = cv2.adaptiveThreshold(frame_processed,maxValue,exec(_Command_adaptiveMethod),exec(_Command_thresholdType),blockSize,C_Value)
    #                   print("Adaptive Theshold executed")
    #                   display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                   frame_buffer.append(frame_processed)
    #           case "bitwise_not":
    #               active = function_parameter['active']
    #               if active:
    #                   frame_processed = cv2.bitwise_not(frame_processed)
    #                   print("bitwise_not executed")
    #                   display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                   frame_buffer.append(frame_processed)

    #           case "BGR2GRAY":
    #               active = function_parameter['active']
    #               if active:
    #                 if len(frame_processed.shape)==3:
    #                   frame_processed = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2GRAY)
    #                   display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                   frame_buffer.append(frame_processed)
    #                   print("BGR2GRAY executed")
    #                 else:
    #                   print("BGR2GRAY ignored! Image is already Grayscale!")

    #           case "ROI":
    #               active = function_parameter['active']
    #               if active:
    #                 if not self.ROI_used:
    #                   ROI_center_x_c = function_parameter['ROI_center_x']
    #                   ROI_center_y_c = function_parameter['ROI_center_y']
    #                   ROI_height = function_parameter['ROI_height']
    #                   ROI_width = function_parameter['ROI_width']
    #                   ROI_center_x_i, ROI_center_y_i = self.CS_Camera_TO_Image(ROI_center_x_c,ROI_center_y_c)
    #                   ROI_center_x_pix, ROI_center_y_pix = self.CS_Image_TO_Pixel(ROI_center_x_i, ROI_center_y_i)
    #                   ROI_half_height_pix = int(round(self.pixelPROum*ROI_height/2))
    #                   ROI_half_width_pix = int(round(self.pixelPROum*ROI_width/2))
    #                   ROI_top_left_x_pix = ROI_center_x_pix - ROI_half_width_pix
    #                   ROI_bottom_right_x_pix = ROI_center_x_pix + ROI_half_width_pix
    #                   ROI_top_left_y_pix = ROI_center_y_pix + ROI_half_height_pix
    #                   ROI_bottom_right_y_pix = ROI_center_y_pix - ROI_half_height_pix
    #                   self.ROI_CS_CV_top_left_x, self.ROI_CS_CV_top_left_y = self.CS_Conv_Pixel_Center_TO_Top_Left(frame_processed.shape[1], frame_processed.shape[0], ROI_top_left_x_pix, ROI_top_left_y_pix)
    #                   self.ROI_CS_CV_bottom_right_x, self.ROI_CS_CV_bottom_right_y = self.CS_Conv_Pixel_Center_TO_Top_Left(frame_processed.shape[1], frame_processed.shape[0], ROI_bottom_right_x_pix, ROI_bottom_right_y_pix)
    #                   if self.ROI_CS_CV_top_left_x>0 and self.ROI_CS_CV_top_left_y>0 and self.ROI_CS_CV_bottom_right_x <= self.img_width and self.ROI_CS_CV_bottom_right_y <= self.img_height:
    #                     frame_processed = frame_processed[self.ROI_CS_CV_top_left_y:self.ROI_CS_CV_bottom_right_y, self.ROI_CS_CV_top_left_x:self.ROI_CS_CV_bottom_right_x]
    #                     self.ROI_used = True
    #                     cv2.rectangle(frame_visual_elements,(self.ROI_CS_CV_top_left_x,self.ROI_CS_CV_top_left_y),(self.ROI_CS_CV_bottom_right_x,self.ROI_CS_CV_bottom_right_y),(240,32,160),3)
    #                     display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                     print("ROI executed")
    #                   else:
    #                     self.VisionOK=False
    #                     self.vision_node.get_logger().error('ROI failed! Out of bounds')
    #                 else:
    #                   self.vision_node.get_logger().warning('ROI already used! ROI can only be applied once!')

    #           case "Canny":
    #             active = function_parameter['active']
    #             threshold1 = function_parameter['threshold1']
    #             threshold2 = function_parameter['threshold2']
    #             aperatureSize = function_parameter['aperatureSize']
    #             L2gradient = function_parameter['L2gradient']
    #             if active:
    #                 frame_processed = cv2.Canny(frame_processed,threshold1,threshold2,aperatureSize)
    #                 print("Canny executed")
    #                 display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                 frame_buffer.append(frame_processed)

    #           case "findContours":
    #             active = function_parameter['active']
    #             draw_contours = function_parameter['draw_contours']
    #             mode = function_parameter['mode']
    #             method = function_parameter['method']
    #             fill = function_parameter['fill']
    #             if active:
    #                 _Command_mode = "cv2." + mode
    #                 _Command_method = "cv2." + method
    #                 #contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), exec(_Command_method))  # Keine Ahnung warum das nicht funktioniert!!!
    #                 #print(_Command_method)
    #                 contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), cv2.CHAIN_APPROX_SIMPLE)
    #                 if fill:
    #                   cv2.fillPoly(frame_processed,pts=contours,color=(255,255,255))
    #                   display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                   frame_buffer.append(frame_processed)
    #                 if draw_contours:
    #                   cv2.drawContours(frame_visual_elements, contours, -1, (0,255,75), 2)
    #                 print("findContours executed")
    #           case "minEnclosingCircle":
    #             active = function_parameter['active']
    #             draw_circles = function_parameter['draw_circles']
    #             mode = function_parameter['mode']
    #             method = function_parameter['method']
    #             if active:
    #               try:
    #                 contours,hierarchy = cv2.findContours(frame_processed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #                 print("Number of contours detected:", len(contours))
    #                 # select the first contour
    #                 cnt = contours[0]
    #                 (x_tl_roi, y_tl_roi),radius = cv2.minEnclosingCircle(cnt)
    #                 x_cs_camera, y_cs_camera = self.CS_CV_TO_camera_with_ROI(int(round(x_tl_roi)),int(round(y_tl_roi)))
    #                 radius_um=radius*self.umPROpixel
    #                 print(str(self.camera_axis_1)+'-Coordinate:'+ str(x_cs_camera))
    #                 print(str(self.camera_axis_2)+'-Coordinate:'+ str(y_cs_camera))
    #                 print('Radius: '+ str(radius_um))
    #                 Circle_result_dict={"Circle":{
    #                   'axis_1': x_cs_camera,
    #                   'axis_2': y_cs_camera,
    #                   'axis_1_suffix': self.camera_axis_1,
    #                   'axis_2_suffix': self.camera_axis_2,
    #                   "radius":radius_um,
    #                   "Unit": "um"
    #                   }}
    #                 if draw_circles:
    #                   x_tl,y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(int(round(x_tl_roi)),int(round(y_tl_roi)))
    #                   # Draw the circumference of the circle.

    #                   cv2.circle(frame_visual_elements, (x_tl, y_tl), int(round(radius)), (0, 255, 0), 2)
    #                   # Draw a small circle (of radius 1) to show the center.
    #                   cv2.circle(frame_visual_elements, (x_tl, y_tl), 1, (0, 0, 255), 2)
    #                 vision_results_list.append(Circle_result_dict)
    #                 print("minEnclosingCircle executed")
    #               except:
    #                 self.VisionOK=False
    #                 self.vision_node.get_logger().error('Min Enclosing Circle detection failed! Image may not be grayscale!')

    #           case "HoughLinesP":
    #             active = function_parameter['active']
    #             threshold = function_parameter['threshold']
    #             minLineLength = function_parameter['minLineLength']
    #             maxLineGap = function_parameter['maxLineGap']
    #             if active:
    #               HoughLinesP_results_list=[]
    #               #print(type(HoughLinesP_results_list))
    #               lines = cv2.HoughLinesP(frame_processed,rho = 1,theta = 1*np.pi/180,threshold = threshold,minLineLength = minLineLength,maxLineGap = maxLineGap)
    #               if lines is not None:
    #                 for x1,y1,x2,y2 in lines[0]:
    #                   x1,y1 = self.CS_Conv_ROI_Pix_TO_Img_Pix(x1,y1)
    #                   x2,y2 = self.CS_Conv_ROI_Pix_TO_Img_Pix(x2,y2)
    #                   cv2.line(frame_visual_elements,(x1,y1),(x2,y2),(0,255,0),2)

    #                   x1_cs_camera, y1_cs_camera = self.CS_CV_TO_camera_with_ROI(x1,y1)
    #                   x2_cs_camera, y2_cs_camera = self.CS_CV_TO_camera_with_ROI(x2,y2)

    #                   print('Point 1 - ' + str(self.camera_axis_1)+'-Coordinate:'+ str(x1_cs_camera))
    #                   print('Point 1 - ' + str(self.camera_axis_2)+'-Coordinate:'+ str(y1_cs_camera))
    #                   print('Point 2 - ' + str(self.camera_axis_1)+'-Coordinate:'+ str(x2_cs_camera))
    #                   print('Point 2 - ' + str(self.camera_axis_2)+'-Coordinate:'+ str(y2_cs_camera))

    #                   HoughLinesP_results_list.append({
    #                     'Point_1': {'axis_1': x1_cs_camera,"axis_2":y2_cs_camera},
    #                     'Point_2': {'axis_1': x2_cs_camera,"axis_2":y2_cs_camera},
    #                     'axis_1_suffix': self.camera_axis_1,
    #                     'axis_2_suffix': self.camera_axis_2,
    #                     'angle': "to be added",
    #                     'length': "to be added",
    #                     "Unit": "um",
    #                     "angle_unit": "degree"
    #                     })

    #                 #print(HoughLinesP_results_list)
    #                 HoughLinesP_results_dict={"Lines": HoughLinesP_results_list}
    #                 vision_results_list.append(HoughLinesP_results_dict)
    #                 print(vision_results_list)

    #               else:
    #                 self.VisionOK=False
    #                 self.counter_error_cross_val += 1
    #                 self.vision_node.get_logger().error('No Line detected!')
    #               print("HoughLinesP executed")

    #           case "select_Area":
    #             active = function_parameter['active']
    #             mode = function_parameter['mode']
    #             method = function_parameter['method']
    #             max_area = function_parameter['max_area']
    #             min_area = function_parameter['min_area']
    #             if active:
    #                 _Command_mode = "cv2." + mode
    #                 _Command_method = "cv2." + method
    #                 #contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), exec(_Command_method))  # Keine Ahnung warum das nicht funktioniert!!!
    #                 contours, hierarchy  = cv2.findContours(frame_processed, exec(_Command_mode), cv2.CHAIN_APPROX_SIMPLE)
    #                 all_areas= []
    #                 for cnt in contours:
    #                     area= cv2.contourArea(cnt)
    #                     all_areas.append(area)
    #                 contour_frame = np.zeros((frame_processed.shape[0], frame_processed.shape[1]), dtype = np.uint8)
    #                 self.VisionOK = False
    #                 for index, area_item in enumerate(all_areas):

    #                     if area_item<max_area and area_item>min_area:
    #                       frame_processed = cv2.drawContours(contour_frame, contours, index, color=(255,255,255), thickness=cv2.FILLED)
    #                       self.VisionOK = True

    #                 if not self.VisionOK:
    #                   self.VisionOK = False
    #                   self.counter_error_cross_val += 1
    #                   print("No matching Area")
    #                 display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #                 frame_buffer.append(frame_processed)
    #                 print("select_Area executed")

    #           case "Morphology_Ex_Opening":
    #             active = function_parameter['active']
    #             kernelsize = function_parameter['kernelsize']

    #             if active:
    #               kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
    #               frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_OPEN, kernel)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Morphology_Ex_Opening executed")

    #           case "Morphology_Ex_Closing":
    #             active = function_parameter['active']
    #             kernelsize = function_parameter['kernelsize']

    #             if active:
    #               kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
    #               frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_CLOSE, kernel)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Morphology_Ex_Closing executed")

    #           case "Horizontal":
    #             active = function_parameter['active']
    #             h_kernelsize = function_parameter['h_kernelsize']

    #             if active:
    #               horizontal_size = received_frame.shape[1] // h_kernelsize
    #               horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    #               frame_processed = cv2.erode(frame_processed, horizontalStructure)
    #               frame_processed = cv2.dilate(frame_processed, horizontalStructure)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Horizontal executed")

    #           case "Vertical":
    #             active = function_parameter['active']
    #             v_kernelsize = function_parameter['v_kernelsize']

    #             if active:
    #               vertical_size = received_frame.shape[0] // v_kernelsize
    #               verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
    #               frame_processed = cv2.erode(frame_processed, verticalStructure)
    #               frame_processed = cv2.dilate(frame_processed, verticalStructure)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Horizontal executed")

    #           case "Blur":
    #             active = function_parameter['active']
    #             kernelsize = function_parameter['kernelsize']
    #             blur_type = function_parameter['type']

    #             if active:
    #               if blur_type == "GaussianBlur":
    #                 frame_processed = cv2.GaussianBlur(frame_processed, (kernelsize, kernelsize),0)
    #               elif blur_type == "Blur":
    #                 frame_processed = cv2.blur(frame_processed, (kernelsize, kernelsize))
    #               elif blur_type == "medianBlur":
    #                 frame_processed = cv2.medianBlur(frame_processed, kernelsize)
    #               else:
    #                 self.vision_node.get_logger().error('Blur type not supported!')
    #                 self.VisionOK = False

    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Blur executed")

    #           case "Morphology_Ex_Gradient":
    #             active = function_parameter['active']
    #             kernelsize = function_parameter['kernelsize']

    #             if active:
    #               kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
    #               frame_processed = cv2.morphologyEx(frame_processed, cv2.MORPH_GRADIENT, kernel)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Morphology_Ex_Gradient executed")

    #           case "Errosion":
    #             active = function_parameter['active']
    #             kernelsize = function_parameter['kernelsize']
    #             iterations = function_parameter['iterations']

    #             if active:
    #               kernel = np.ones((kernelsize, kernelsize), np.uint8)
    #               frame_processed = cv2.erode(frame_processed, kernel, iterations=iterations)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Errosion executed")

    #           case "Dilation":
    #             active = function_parameter['active']
    #             kernelsize = function_parameter['kernelsize']
    #             iterations = function_parameter['iterations']

    #             if active:
    #               kernel = np.ones((kernelsize, kernelsize), np.uint8)
    #               frame_processed = cv2.dilate(frame_processed, kernel, iterations=iterations)
    #               display_frame=self.adaptImagewithROI(display_frame,frame_processed)
    #               frame_buffer.append(frame_processed)
    #               print("Dilation executed")

    #           case "save_image":
    #             active = function_parameter['active']
    #             prefix = function_parameter['prefix']
    #             with_vision_elements = function_parameter['with_vision_elements']
    #             save_in_cross_val = function_parameter['save_in_cross_val']
    #             if active:

    #                 if not os.path.exists(self.process_db_path):
    #                   os.makedirs(self.process_db_path)
    #                   print("Process DB folder created!")

    #                 image_name=self.process_db_path+"/"+self.vision_process_id+"_"+self.process_start_time+prefix+".png"

    #                 if not os.path.isfile(image_name) and (not self.cross_val_running or save_in_cross_val):
    #                   if with_vision_elements:
    #                     display_frame = self.adaptImagewithROI(display_frame,frame_processed)
    #                     image_to_save = self.create_vision_element_overlay(display_frame,frame_visual_elements)
    #                   else:
    #                       image_to_save = frame_processed
    #                   cv2.imwrite(image_name,image_to_save)
    #                   print("Image saved!")
    #                 print("save_image executed")

    #           case "Draw_Grid_without_rotation":
    #             active = function_parameter['active']
    #             grid_spacing = function_parameter['grid_spacing']
    #             if active:
    #                 numb_horizontal = int(round((self.FOV_height/2)/grid_spacing))+1
    #                 numb_vertical = int(round((self.FOV_width/2)/grid_spacing))+1
    #                 cv2.putText(img=frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)

    #                 cv2.line(frame_visual_elements, (int(display_frame.shape[1]/2), 0),(int(display_frame.shape[1]/2), display_frame.shape[1]), (255, 0, 0), 1, 1)
    #                 cv2.line(frame_visual_elements, (0,int(display_frame.shape[0]/2)),(int(display_frame.shape[1]), int(display_frame.shape[0]/2)), (255, 0, 0), 1, 1)
    #                 #Draw horizontal lines
    #                 for numb_h in range(numb_horizontal):
    #                   pixel_delta=int(numb_h*grid_spacing*self.pixelPROum)
    #                   cv2.line(frame_visual_elements, (0,int(display_frame.shape[0]/2)+pixel_delta),(int(display_frame.shape[1]), int(display_frame.shape[0]/2)+pixel_delta), (255, 0, 0), 1, 1)
    #                   cv2.line(frame_visual_elements, (0,int(display_frame.shape[0]/2)-pixel_delta),(int(display_frame.shape[1]), int(display_frame.shape[0]/2)-pixel_delta), (255, 0, 0), 1, 1)
    #                 # draw vertical lines
    #                 for numb_v in range(numb_vertical):
    #                   pixel_delta=int(numb_v*grid_spacing*self.pixelPROum)
    #                   cv2.line(frame_visual_elements, (int(display_frame.shape[1]/2)+pixel_delta, 0),(int(display_frame.shape[1]/2)+pixel_delta, display_frame.shape[1]), (255, 0, 0), 1, 1)
    #                   cv2.line(frame_visual_elements, (int(display_frame.shape[1]/2)-pixel_delta, 0),(int(display_frame.shape[1]/2)-pixel_delta, display_frame.shape[1]), (255, 0, 0), 1, 1)
    #                 print("Grid executed")

    #           case "Draw_Grid":
    #             active = function_parameter['active']
    #             grid_spacing = function_parameter['grid_spacing']

    #             if active:
    #               Grid_frame = np.zeros((received_frame.shape[0]+received_frame.shape[1], received_frame.shape[0]+received_frame.shape[1], 3), dtype = np.uint8)
    #               numb = int(round((Grid_frame.shape[0]/2)/grid_spacing*self.pixelPROum))+1

    #               cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2), 0),(int(Grid_frame.shape[1]/2), Grid_frame.shape[1]), (255, 0, 0), 1, 1)
    #               cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)), (255, 0, 0), 1, 1)

    #               for n in range(numb):
    #                 #Draw horizontal lines
    #                 pixel_delta=int(n*grid_spacing*self.pixelPROum)
    #                 cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)+pixel_delta),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)+pixel_delta), (255, 0, 0), 1, 1)
    #                 cv2.line(Grid_frame, (0,int(Grid_frame.shape[0]/2)-pixel_delta),(int(Grid_frame.shape[1]), int(Grid_frame.shape[0]/2)-pixel_delta), (255, 0, 0), 1, 1)
    #                 # draw vertical lines
    #                 cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2)+pixel_delta, 0),(int(Grid_frame.shape[1]/2)+pixel_delta, Grid_frame.shape[1]), (255, 0, 0), 1, 1)
    #                 cv2.line(Grid_frame, (int(Grid_frame.shape[1]/2)-pixel_delta, 0),(int(Grid_frame.shape[1]/2)-pixel_delta, Grid_frame.shape[1]), (255, 0, 0), 1, 1)

    #               Grid_frame= rotate_image(Grid_frame,self.camera_axis_1_angle)
    #               center = Grid_frame.shape
    #               x = center[1]/2 - self.img_width/2
    #               y = center[0]/2 - self.img_height/2

    #               crop_img = Grid_frame[int(y):int(y+self.img_height), int(x):int(x+self.img_width)]
    #               frame_visual_elements = self.create_vision_element_overlay(frame_visual_elements,crop_img)
    #               cv2.putText(img=frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)
    #               print("Grid executed")

    #           case "Draw_CS":
    #             active = function_parameter['active']
    #             if active:
    #               # Does not work for alpha >90 yet
    #               CS_frame = np.zeros((received_frame.shape[0]+received_frame.shape[1], received_frame.shape[0]+received_frame.shape[1], 3), dtype = np.uint8)
    #               if self.camera_axis_1 == 'z' or self.camera_axis_1 == 'Z':
    #                 color_axis_1 = (255, 0, 0)
    #               elif self.camera_axis_1 == 'y' or self.camera_axis_1 == 'Y':
    #                 color_axis_1 = (0, 255, 0)
    #               else:
    #                 color_axis_1 = (0, 0, 255)

    #               if self.camera_axis_2 == 'z' or self.camera_axis_2 == 'Z':
    #                 color_axis_2 = (255, 0, 0)
    #               elif self.camera_axis_2 == 'x' or self.camera_axis_2 == 'X':
    #                 color_axis_2 = (0, 0, 255)
    #               else:
    #                 color_axis_2 = (0, 255, 0)

    #               #draw axis_1
    #               cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(CS_frame.shape[1], int(CS_frame.shape[0]/2)), color_axis_1, 2, 1)
    #               #draw axis_2
    #               if self.camera_axis_2_angle == '+':
    #                 cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(int(CS_frame.shape[1]/2), 0), color_axis_2, 2, 1)
    #               else:
    #                 cv2.line(CS_frame, (int(CS_frame.shape[1]/2), int(CS_frame.shape[0]/2)),(int(CS_frame.shape[1]/2), CS_frame.shape[0]), color_axis_2 , 2, 1)
    #               CS_frame= rotate_image(CS_frame,self.camera_axis_1_angle)
    #               center = CS_frame.shape
    #               x = center[1]/2 - self.img_width/2
    #               y = center[0]/2 - self.img_height/2
    #               crop_img = CS_frame[int(y):int(y+self.img_height), int(x):int(x+self.img_width)]
    #               frame_visual_elements = self.create_vision_element_overlay(frame_visual_elements,crop_img)
    #               print("Draw_CS executed!")

    #           case "Draw_Grid_TO_BE_DELETED":
    #             active = function_parameter['active']
    #             grid_spacing = function_parameter['grid_spacing']

    #             if active:
    #               numb_horizontal = int(round((self.FOV_height/2)/grid_spacing))+1
    #               numb_vertical = int(round((self.FOV_width/2)/grid_spacing))+1
    #               cv2.putText(img=frame_visual_elements,text="Grid: "+ str(grid_spacing) + "um", org=(5,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0), thickness=1)

    #               # vertical center line
    #               p_x_centerline=-1*int(round(math.tan(degrees_to_rads(self.camera_axis_1_angle))*round(display_frame.shape[0]/2)))
    #               p_y_centerline=int(round(display_frame.shape[0]/2))
    #               p1_x_v_centerline_tl, p1_y_v_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],p_x_centerline,p_y_centerline)
    #               p2_x_v_centerline_tl, p2_y_v_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],-p_x_centerline,-p_y_centerline)
    #               cv2.line(frame_visual_elements, (p1_x_v_centerline_tl, p1_y_v_centerline_tl),(p2_x_v_centerline_tl, p2_y_v_centerline_tl), (255, 0, 0), 1, 1)

    #               # horizontal center line
    #               p_y_centerline=int(round(math.tan(degrees_to_rads(self.camera_axis_1_angle))*round(display_frame.shape[1]/2)))
    #               p_x_centerline=int(round(display_frame.shape[1]/2))
    #               p1_x_h_centerline_tl, p1_y_h_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],p_x_centerline,p_y_centerline)
    #               p2_x_h_centerline_tl, p2_y_h_centerline_tl = self.CS_Conv_Pixel_Center_TO_Top_Left(display_frame.shape[1],display_frame.shape[0],-p_x_centerline,-p_y_centerline)
    #               cv2.line(frame_visual_elements, (p1_x_h_centerline_tl, p1_y_h_centerline_tl),(p2_x_h_centerline_tl, p2_y_h_centerline_tl), (255, 0, 0), 1, 1)

    #               # draw horizontal lines
    #               grid_spacing_t = int(round(math.cos(degrees_to_rads(self.camera_axis_1_angle))*grid_spacing*self.pixelPROum))

    #               for numb_h in range(numb_horizontal):
    #                 cv2.line(frame_visual_elements, (p1_x_h_centerline_tl, p1_y_h_centerline_tl+numb_h*grid_spacing_t),(p2_x_h_centerline_tl, p2_y_h_centerline_tl+numb_h*grid_spacing_t), (255, 0, 0), 1, 1)
    #                 cv2.line(frame_visual_elements, (p1_x_h_centerline_tl, p1_y_h_centerline_tl-numb_h*grid_spacing_t),(p2_x_h_centerline_tl, p2_y_h_centerline_tl-numb_h*grid_spacing_t), (255, 0, 0), 1, 1)
    #               # draw vertical lines
    #               for numb_v in range(numb_vertical):
    #                 pixel_delta=int(numb_v*grid_spacing*self.pixelPROum)
    #                 cv2.line(frame_visual_elements, (p1_x_v_centerline_tl+grid_spacing_t*numb_v, p1_y_v_centerline_tl),(p2_x_v_centerline_tl+grid_spacing_t*numb_v, p2_y_v_centerline_tl), (255, 0, 0), 1, 1)
    #                 cv2.line(frame_visual_elements, (p1_x_v_centerline_tl-grid_spacing_t*numb_v, p1_y_v_centerline_tl),(p2_x_v_centerline_tl-grid_spacing_t*numb_v, p2_y_v_centerline_tl), (255, 0, 0), 1, 1)
    #               print("Grid executed2")

    #           case "HoughCircles":
    #               active = function_parameter['active']
    #               draw_circles = function_parameter['draw_circles']
    #               method = function_parameter['method']
    #               dp = function_parameter['dp']
    #               minDist = function_parameter['minDist']
    #               param1 = function_parameter['param1']
    #               param2 = function_parameter['param2']
    #               minRadius = int(round(function_parameter['minRadius']* self.pixelPROum)) # conv in Pixel
    #               maxRadius = int(round(function_parameter['maxRadius']* self.pixelPROum)) # conv in Pixel
    #               if active:
    #                 _Command_method = "cv2." + method
    #                 #print(_Command_method)
    #                 try:
    #                   detected_circles = cv2.HoughCircles(frame_processed,cv2.HOUGH_GRADIENT, dp, minDist, param1 = param1,param2 = param2, minRadius = minRadius, maxRadius = maxRadius)
    #                   if detected_circles is not None:
    #                     print("Cirlces Detected")
    #                     # Convert the circle parameters a, b and r to integers.
    #                     detected_circles = np.uint16(np.around(detected_circles))
    #                     HoughCircles_reslults_list=[]
    #                     for pt in detected_circles[0, :]:
    #                       x, y, r = pt[0], pt[1], pt[2]

    #                       x_cs_camera, y_cs_camera = self.CS_CV_TO_camera_with_ROI(x,y)
    #                       radius_um=r*self.umPROpixel
    #                       print(str(self.camera_axis_1)+'-Coordinate:'+ str(x_cs_camera))
    #                       print(str(self.camera_axis_2)+'-Coordinate:'+ str(y_cs_camera))
    #                       print('Radius: '+ str(radius_um))
    #                       HoughCircles_reslults_list.append({
    #                         'axis_1': x_cs_camera,
    #                         'axis_2': y_cs_camera,
    #                         'axis_1_suffix': self.camera_axis_1,
    #                         'axis_2_suffix': self.camera_axis_2,
    #                         "radius":radius_um,
    #                         "Unit": "um"
    #                         })

    #                       if draw_circles:
    #                         x_tl,y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(x,y)
    #                         # Draw the circumference of the circle.
    #                         cv2.circle(frame_visual_elements, (x_tl, y_tl), r, (0, 255, 0), 2)
    #                         # Draw a small circle (of radius 1) to show the center.
    #                         cv2.circle(frame_visual_elements, (x_tl, y_tl), 1, (0, 0, 255), 2)
    #                     HouchCircles_results_dict={"Circles": HoughCircles_reslults_list}
    #                     vision_results_list.append(HouchCircles_results_dict)
    #                   else:
    #                     self.VisionOK=False
    #                     self.counter_error_cross_val += 1
    #                     self.vision_node.get_logger().error('No circle detected!')
    #                   print("Hough Circles executed")
    #                 except:
    #                   self.VisionOK=False
    #                   self.vision_node.get_logger().error('Circle detection failed! Image may not be grayscale!')

    #     if self.VisionOK:
    #       self.vision_node.get_logger().info('Vision process executed cleanly!')
    #     else:
    #       self.vision_node.get_logger().error('Vision process executed with error!')
    #   except:
    #       self.vision_node.get_logger().error("Fatal Error in vision function! Contact maintainer!")

    #   if not self.VisionOK:
    #     cv2.rectangle(frame_visual_elements,(0,0),(frame_visual_elements.shape[1],frame_visual_elements.shape[0]),(0,0,255),3)
    #   else:
    #     cv2.rectangle(frame_visual_elements,(0,0),(frame_visual_elements.shape[1],frame_visual_elements.shape[0]),(0,255,0),3)

    #   # Add the vision_results_list to the vision_results_file
    #   vision_results_file_dict["vision_results"] = vision_results_list
    #   # Save the vision_results_file
    #   self.save_vision_results(vision_results_file_dict)

    #   display_frame=self.create_vision_element_overlay(display_frame,frame_visual_elements)

    #   if len(received_frame.shape)<3:
    #     received_frame = cv2.cvtColor(received_frame,cv2.COLOR_GRAY2BGR)

    #   if  self.show_input_and_output_image:
    #     display_frame = cv2.vconcat([received_frame,display_frame])

    #   display_frame=image_resize(display_frame, height = (self.screen_height-100))

    #   return display_frame


def main(args=None):
    pass


if __name__ == "__main__":
    main()
