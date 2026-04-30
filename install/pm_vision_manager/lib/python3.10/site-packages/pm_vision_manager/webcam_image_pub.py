# Basic ROS 2 program to publish real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
  
# Import the necessary libraries
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
from pm_vision_interfaces.srv import DemoSetExposure

import time

class ImagePublisher(Node):
  """
  Create an ImagePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('webcam_image_publisher')
      
    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
  
    self.frame_count = 0
    self.last_time = time.time()
        

    # We will publish a message every 0.1 seconds
    timer_period = 0.030  # ~30 fps
    self.timer = self.create_timer(timer_period, self.timer_callback)
      
    # Create the timer
    self.timer = self.create_timer(timer_period, self.timer_callback)
    self.exposure_clinet = self.create_service(DemoSetExposure,f"{self.get_name()}/demo_set_exposure",self.set_exposure)

    # Create a VideoCapture object
    # The argument '0' gets the default webcam.
    self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        
    self.cap.set(cv2.CAP_PROP_FPS, 60)
    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not self.cap.isOpened():
      self.get_logger().error("❌ Cannot open webcam!")
      raise RuntimeError("Cannot open camera")

    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
     
  def set_exposure(self,request: DemoSetExposure.Request, response: DemoSetExposure.Response):
    self.get_logger().warn(f"exposure time set to {request.target_value}")
    response.success = True
    return response
  
  def timer_callback(self):
    """
    Callback function.
    This function gets called every 0.1 seconds.
    """
    # Capture frame-by-frame
    # This method returns True/False as well
    # as the video frame.
    ret, frame = self.cap.read()
    
    if ret:
      try:
        # Convert to ROS message and publish
        img_msg = self.br.cv2_to_imgmsg(frame, encoding="bgr8")
        self.publisher_.publish(img_msg)
        
        # FPS calculation
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 2.0:
          fps = self.frame_count / (current_time - self.last_time)
          self.get_logger().info(f'Publishing at {fps*2:.1f} FPS')
          self.frame_count = 0
          self.last_time = current_time
              
      except Exception as e:
        self.get_logger().error(f'Error: {str(e)}')
    else:
      self.get_logger().warning('Failed to capture frame')

def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_publisher = ImagePublisher()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_publisher)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_publisher.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()