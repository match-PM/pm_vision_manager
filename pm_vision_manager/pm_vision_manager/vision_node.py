# Import the necessary libraries
import rclpy  # Python Client Library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
import cv2
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QSizePolicy
from PyQt6.QtGui import QColor, QTextCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QByteArray
from threading import Thread 
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
import time
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
import sys
from pm_vision_manager.va_py_modules.vision_utils import get_screen_resolution, image_resize
from copy import copy
from pm_vision_interfaces.srv import ExecuteVision
from pm_vision_interfaces.srv import StopVisionAssistant
from pm_vision_interfaces.srv import StartVisionAssistant
from pm_vision_interfaces.srv import GetRunningAssistants
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
from geometry_msgs.msg import Point

class VisionNode(Node):
    """
    Create an ImagePublisher class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        super().__init__("vision_assistant")

        self.callback_group = ReentrantCallbackGroup()
        self.callback_group_image_subscriptions = MutuallyExclusiveCallbackGroup()
        self.br = CvBridge()
        self.image_list = []
        self.running_vision_assistants = []
        self.execute_vision_srv = self.create_service(
            ExecuteVision,
            f"{self.get_name()}/ExecuteVision",
            self.execute_vision,
            callback_group=self.callback_group,
        )
        self.start_assistant_srv = self.create_service(
            StartVisionAssistant,
            f"{self.get_name()}/StartVisionAssistant",
            self.start_vision_assistant,
            callback_group=self.callback_group,
        )
        self.stop_assistant_vision_srv = self.create_service(
            StopVisionAssistant,
            f"{self.get_name()}/StopVisionAssistant",
            self.stop_vision_assistant,
            callback_group=self.callback_group,
        )
        self.get_running_assistants_srv = self.create_service(
            GetRunningAssistants,
            f"{self.get_name()}/GetRunningAssistants",
            self.get_running_assistants,
            callback_group=self.callback_group,
        )
        self.timer = self.create_timer(0.5, self.display_image_callback, callback_group=self.callback_group)

        self.screen_resolution = get_screen_resolution()
        self.screen_height = int(self.screen_resolution["height"].decode("UTF-8"))
        self.screen_width = int(self.screen_resolution["width"].decode("UTF-8"))
        self.get_logger().info(f"Screen resolution: {str(self.screen_width)}x{str(self.screen_height)}")

        self.pub = self.create_publisher(Image, f"VisionManager/test", 10)
        self.get_logger().info("Vision node started!")
        self.image_widgets = {}

    def execute_vision(self, request: ExecuteVision.Request, response: ExecuteVision.Response):
        VisionProcess = VisionProcessClass(
            self,
            launch_as_assistant=False,
            process_filename=request.process_filename,
            camera_config_filename=request.camera_config_filename,
            db_cross_val_only=request.db_cross_val_only,
            process_UID=request.process_uid,
            image_display_time_visualization=request.image_display_time,
            open_process_file=False,
            run_cross_validation=request.run_cross_validation, # TODO Was ist request?
            show_image_on_error=False,
            step_through_images=False,
        )

        if VisionProcess.init_success:
            response.success = True
        else:
            self.get_logger().error(
                "Error initializing service request. Service aboarted!"
            )
            response.success = False
            return response

        while not VisionProcess.delete_this_object:
            time.sleep(0.5)

        response.success = VisionProcess.image_processing_handler.get_vision_ok()
        response.process_uid = request.process_uid
        response.results_dict = str(VisionProcess.results_dict)
        response.results_path = str(VisionProcess.vision_results_path)
        del VisionProcess
        
        point1 = Point()
        point1.x = 1.5
        point1.y = 2.5
        point1.z = 3.5

        point2 = Point()
        point2.x = 4.5
        point2.y = 5.5
        point2.z = 6.5        
        response.points.append(point1)
        response.points.append(point2)
        return response

    def start_vision_assistant(
        self,
        request: StartVisionAssistant.Request,
        response: StartVisionAssistant.Response,
    ):
        try:
            for tpl in self.running_vision_assistants:
                if tpl[0] == request.process_uid:
                    self.get_logger().error(
                        f"Vision Assistant cannot be launched because a process with id: {tpl[0]} is already running!"
                    )
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
                run_cross_validation=request.run_cross_validation,
                show_image_on_error=request.show_image_on_error,
                step_through_images=request.step_through_images,
            )

            if VisionProcess.init_success:
                self.running_vision_assistants.append(
                    (request.process_uid, VisionProcess)
                )
                response.success = True
            else:
                self.get_logger().error(
                    "Error initializing service request. Service aboarted!"
                )
                response.success = False

            response.process_uid = request.process_uid

        except Exception:
            response.success = False
        return response

    def stop_vision_assistant(
        self,
        request: StopVisionAssistant.Request,
        response: StopVisionAssistant.Response,
    ):
        # if request.process_uid in self.running_vision_assistants:
        response.success = False
        self.get_logger().error(f"Stop Vision assistant: {request.process_uid}")

        for index, VisionInstance in enumerate(self.running_vision_assistants):
            # VisionInstance is a douple of name, visionassistantclass
            if VisionInstance[0] == request.process_uid:
                VisionInstance[1].stop_image_subscription = True
                VisionInstance[1].set_display_time_for_exit()
                try:
                    VisionInstance[1].db_thread.join()
                except:
                    pass
                while not VisionInstance[1].delete_this_object:
                    time.sleep(0.5)
                    self.get_logger().debug(f"Stuck in loop of '{request.process_uid}'")
                del self.running_vision_assistants[index]
                self.get_logger().info(
                    f"Vision Assistant: {request.process_uid} stoped!"
                )
                response.success = True
                response.process_uid = request.process_uid
                break

        if not response.success:
            self.get_logger().error(
                f"Vision Assistant with ID {request.process_uid} does not exist!"
            )

        return response

    def get_running_assistants(
        self,
        request: GetRunningAssistants.Request,
        response: GetRunningAssistants.Response,
        ):
        # get list of the first element of the tuple
        list_of_running_assistants = [tpl[0] for tpl in self.running_vision_assistants]
        response.running_assistants = list_of_running_assistants

        return response
    
    def display_image_callback(self)-> None:
        images_to_remove = []
        try:
            # looking for timed out elements
            for index, image_item in enumerate(self.image_list):
                # Access elements within the tuple
                name, image, display_time, start_time = image_item

                if not (display_time == 0) and (
                    self.get_clock().now().nanoseconds / 1e9
                    > start_time.nanoseconds / 1e9 + display_time):
                    images_to_remove.append(image_item)

            # removing timed out elements
            for image_item in images_to_remove:
                self.get_logger().info(f"Closing image: {name}")
                name = image_item[0]
                self.image_list.remove(image_item)
                self.image_widgets[name].destroy()
                del self.image_widgets[name]

            # Creating or updating the image outputs for the list
            for index, image_item in enumerate(self.image_list):
                # Access elements within the tuple
                name, image, display_time, start_time = image_item

                if not display_time == 0:

                    if name not in self.image_widgets:
                        # Create a new widget if it doesn't exist
                        widget = ImageDisplayWidget(name, image, screen_height=self.screen_height)
                        widget.show()
                        self.image_widgets[name] = widget
                        self.get_logger().debug("Creating new image window '{name}'!")
                    else:
                        # Update the existing widget
                        self.image_widgets[name].set_image(image,screen_height=self.screen_height)
                        self.get_logger().warn(f"Updating image window '{name}'!")
                    
                    #self.pub.publish(self.br.cv2_to_imgmsg(image, encoding="rgb8"))
                    QApplication.processEvents()

        except Exception as e:
            self.get_logger().error("Error occurred in displaying image!")
            self.get_logger().error(e)

class ImageDisplayWidget(QWidget):
    def __init__(self, name, image, screen_height = None, parent=None):
        super(ImageDisplayWidget, self).__init__(parent)

        self.setWindowTitle(name)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.set_image(image, screen_height)

    def set_image(self, image, screen_height = None):
        height, width, channel = image.shape

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if screen_height is None:
            screen_height = height

        image = image_resize(image,height=screen_height-100)

        height, width, channel = image.shape

        bytes_per_line = 3 * width

        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.clear()
        self.image_label.setPixmap(pixmap)
        self.image_label.repaint()
        self.update()

def main(args=None):
    # # Initialize the rclpy library
    # rclpy.init(args=args)
    # # Create the node
    # vision_node = VisionNode()
    # executor = MultiThreadedExecutor(num_threads=6)
    # executor.add_node(vision_node)
    # # Spin the node so the callback function is called.
    # executor.spin()

    # executor.shutdown()
    # vision_node.destroy_node()

    # # Shutdown the ROS client library for Python
    # rclpy.shutdown()

    rclpy.init(args=args)
    executor = MultiThreadedExecutor(num_threads=6) 

    app = QApplication(sys.argv)

    vision_node = VisionNode()
    executor.add_node(vision_node)

    thread = Thread(target=executor.spin)
    thread.start()
    
    try:
        sys.exit(app.exec())

    finally:
        
        vision_node.destroy_node()
        executor.shutdown()
        rclpy.shutdown()
        app.closeAllWindows()

if __name__ == "__main__":
    main()
