# Import the necessary libraries
import rclpy  # Python Client Library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
import cv2
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QSizePolicy, QFileDialog
from PyQt6.QtGui import QColor, QTextCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QByteArray, pyqtSignal, QObject
from threading import Thread, Timer
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
import time
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
import sys
import numpy as np
from copy import copy
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
from geometry_msgs.msg import Point
from functools import partial
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from PyQt6.QtGui import QIcon

from pm_vision_interfaces.srv import ExecuteVision, CalibrateAngle, CalibratePixelPerUm
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass
from pm_vision_manager.va_py_modules.vision_utils import get_screen_resolution, image_resize

from pm_vision_manager.va_py_modules.vision_app_modules.VisionAssistantWindow import VisionAssistantWindow
from pm_vision_manager.va_py_modules.vision_app_modules.ImageDisplayWidget import ImageDisplayWidget

from pm_vision_manager.va_py_modules.manager_configuration import (check_for_valid_path_config, 
                                                                   set_process_library_path, 
                                                                   set_camera_config_path, 
                                                                   set_vision_database_path, 
                                                                   set_function_library_path,
                                                                   check_for_valid_inputs)
class CreateVisionInstanceSignal(QObject):
    signal = pyqtSignal(str, VisionProcessClass)

class UpdateInstancesSignal(QObject):
    signal = pyqtSignal()

class NextImageSignal(QObject):
    signal = pyqtSignal()

class DestroyVisionInstanceSignal(QObject):
    signal = pyqtSignal(str)

class AppConfigError(Exception):
    pass

class VisionNode(Node):
    """
    Create an ImagePublisher class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        super().__init__("vision_assistant")

        # Check and set the path configuration for the vision manager
        self.init_app_config()
        
        self.main_window = VisionAssistantWindow(self)
        self.main_window.show()

        self.callback_group = ReentrantCallbackGroup()

        #self.callback_group_image_subscriptions = ReentrantCallbackGroup()
        self.br = CvBridge()
        self.image_list = []
        self.running_vision_assistants = []

        self.execute_vision_srv = self.create_service(
            ExecuteVision,
            f"{self.get_name()}/ExecuteVision",
            self.execute_vision,
            callback_group=self.callback_group,
        )

        self.set_pixel_camera_srv = self.create_service(
            CalibratePixelPerUm,
            f"{self.get_name()}/SetCameraPixelPerUm",
            self.set_camera_pixel_per_um,
            callback_group=self.callback_group,
        )

        self.set_camera_angle_srv = self.create_service(
            CalibrateAngle,
            f"{self.get_name()}/SetCameraAngle",
            self.set_camera_angle,
            callback_group=self.callback_group,
        )

        # self.execute_vision_srv = self.create_service(
        #     ExecuteVision,
        #     f"{self.get_name()}/StartVisionAssistant",
        #     self.start_vision_assistant,
        #     callback_group=self.callback_group,
        # )

        self.screen_resolution = get_screen_resolution()
        self.screen_height = int(self.screen_resolution["height"].decode("UTF-8"))
        self.screen_width = int(self.screen_resolution["width"].decode("UTF-8"))
        self.get_logger().info(f"Screen resolution: {str(self.screen_width)}x{str(self.screen_height)}")
        
        self.pub = self.create_publisher(Image, f"VisionManager/test", 10)
        self.get_logger().info("Vision node started!")
        self.image_widgets = {}
        VisionProcessClass.create_process_folder("Assembly_Manager",logger=self.get_logger())
        VisionProcessClass.create_process_folder("PM_Robot_Calibration",logger=self.get_logger())

    def execute_vision(self, request: ExecuteVision.Request, response: ExecuteVision.Response):

        input_valid = check_for_valid_inputs(request.process_filename, request.camera_config_filename, self.get_logger())
            
        if not input_valid:
            self.get_logger().error("Invalid input for process or camera config file!")
            response.success = False
            return response
        
        try:
            vision_instance = VisionProcessClass(
                self,
                launch_as_assistant=False,
                process_filename=request.process_filename,
                camera_config_filename=request.camera_config_filename,
                process_UID=request.process_uid,
                run_cross_validation=request.run_cross_validation
            )

        except ValueError as e:
            self.get_logger().error(f"Error initializing vision instance: {str(e)}")
            response.success = False
            return response

        # attach the vision instance to the main window
        self.main_window.start_execution_widget_signal.signal.emit(vision_instance,request.image_display_time)
        
        vision_instance.execute_vision()

        response.success = vision_instance.image_processing_handler.get_vision_ok()
        response.vision_response = vision_instance.construct_results_metadata(vision_instance.image_processing_handler.get_vision_response())
        response.results_path = str(vision_instance.vision_results_path)
        
        vision_instance.image_processing_handler.disable_all_lights()
        
        vision_instance.terminate_vision_class()
        del vision_instance
        
        if not response.success:
            self.get_logger().error("Vision execution failed! An instance of the vision assistant will be opened")
            self.main_window.start_vision_assistant_wiget_signal.signal.emit(request.camera_config_filename, 
                                                                            request.process_filename)
        
        return response

    # def start_vision_assistant(self, request: ExecuteVision.Request, response: ExecuteVision.Response):

    #     input_valid = check_for_valid_inputs(request.process_filename, request.camera_config_filename, self.get_logger())
            
    #     if not input_valid:
    #         self.get_logger().error("Invalid input for process or camera config file!")
    #         response.success = False
    #         return response
        
    #     try:
    #         vision_instance = VisionProcessClass(
    #             self,
    #             launch_as_assistant=False,
    #             process_filename=request.process_filename,
    #             camera_config_filename=request.camera_config_filename,
    #             process_UID=request.process_uid,
    #             run_cross_validation=request.run_cross_validation)

    #     except ValueError as e:
    #         self.get_logger().error(f"Error initializing vision instance: {str(e)}")
    #         response.success = False
    #         return response

        
    #     vision_instance.start_vision_subscription()

    #     # attach the vision instance to the main window
    #     self.main_window.start_execution_widget_signal.signal.emit(vision_instance,request.image_display_time)

    #     # Wait for the vision to finish
    #     while not vision_instance.image_processing_handler.stop_vision_execution:
    #         time.sleep(0.5)

    #     response.success = vision_instance.image_processing_handler.get_vision_ok()
    #     response.vision_response = vision_instance.construct_results_metadata(vision_instance.image_processing_handler.get_vision_response())
    #     self.get_logger().warn(f"HEEERREEE Vision response: {response.vision_response}")
    #     response.results_path = str(vision_instance.vision_results_path)
    #     #response.vision_response.results = vision_instance.image_processing_handler.get_vision_response()
    #     del vision_instance

    #     return response


    def init_app_config(self):
        if not check_for_valid_path_config(self.get_logger()):
            self.get_logger().error("Invalid path configuration!")
            # Set config for process library path
            process_folder_path = QFileDialog.getExistingDirectory(None, "Select Folder for the Process Library")
            if process_folder_path == "":
                self.get_logger().error("No path selected for process library!")
                raise AppConfigError("Vision Mangager not configured correctly! Exiting...")
            set_process_library_path(process_folder_path+"/", self.get_logger())
            # Set config for camera config path
            camera_folder_path = QFileDialog.getExistingDirectory(None, "Select Folder for the Camera Config")
            if camera_folder_path == "":
                self.get_logger().error("No path selected for camera config!")
                raise AppConfigError("Vision Mangager not configured correctly! Exiting...")
            set_camera_config_path(camera_folder_path+"/", self.get_logger())
            # Set config for vision database path
            vision_db_path = QFileDialog.getExistingDirectory(None, "Select Folder for the Vision Database")
            if vision_db_path == "":
                self.get_logger().error("No path selected for vision database!")
                raise AppConfigError("Vision Mangager not configured correctly! Exiting...")
            set_vision_database_path(vision_db_path+"/", self.get_logger())
            # Set config for function library path

            function_library_path = f"{get_package_share_directory('pm_vision_manager')}/vision_functions"

            # function_library_path = QFileDialog.getExistingDirectory(None, "Select Folder for the Function Library")
            # if function_library_path == "":
            #     self.get_logger().error("No path selected for function library!")
            #     raise AppConfigError("Vision Mangager not configured correctly! Exiting...")
            
            set_function_library_path(function_library_path+"/", self.get_logger())
            
            if not check_for_valid_path_config(self.get_logger()):
                raise AppConfigError("Vision Mangager not configured correctly! Exiting...")
            
    def set_camera_pixel_per_um(self,request: CalibratePixelPerUm.Request, response: CalibratePixelPerUm.Response):
        """
        Set the camera pixel per um value in the camera config file.
        """

        if not check_for_valid_path_config(self.get_logger()):
            self.get_logger().error("Invalid path configuration!")
            return False
        
        set_success = VisionProcessClass.correct_camera_pixel_per_um(request.camera_config_file_name,
                                                                    request.multiplicator,
                                                                    self.get_logger())
        
        response.success = set_success
        return response
    
    def set_camera_angle(self, request: CalibrateAngle.Request, response: CalibrateAngle.Response):
        """
        Set the camera angle in the camera config file.
        """

        if not check_for_valid_path_config(self.get_logger()):
            self.get_logger().error("Invalid path configuration!")
            return False
        
        set_success = VisionProcessClass.correct_camera_angle(request.camera_config_file_name,
                                                              request.angle_diff,
                                                              self.get_logger())
        
        response.success = set_success
        
        return response
            
def main(args=None):

    rclpy.init(args=args)
    executor = MultiThreadedExecutor(num_threads=6) 
    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(f"{get_package_share_directory('pm_vision_manager')}/app_icon.png"))

        vision_node = VisionNode()

        executor.add_node(vision_node)
        
        thread = Thread(target=executor.spin)
        thread.start()       

        sys.exit(app.exec())

    except AppConfigError as e:
        app.closeAllWindows()
        executor.shutdown()
        rclpy.shutdown()

    except KeyboardInterrupt as e:
        app.closeAllWindows()
        vision_node.destroy_node()
        executor.shutdown()
        rclpy.shutdown()
        
    finally:
        app.closeAllWindows()
        vision_node.destroy_node()
        executor.shutdown()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
