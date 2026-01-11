import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('webcam_image_publisher')
        print("=== Starting Webcam Publisher ===")
        
        # Create publisher
        self.publisher_ = self.create_publisher(Image, 'video_frames', 1)
        
        # For FPS calculation
        self.frame_count = 0
        self.last_time = time.time()
        
        # Timer for maximum FPS
        timer_period = 0.030  # ~30 fps
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Open the camera with V4L2 backend
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        
        if not self.cap.isOpened():
            self.get_logger().error("❌ Cannot open webcam!")
            raise RuntimeError("Cannot open camera")
        
        # UGREEN 2K Camera Settings - Try different combinations:
        
        # Option A: Higher FPS with lower resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        
        # Option B: Even higher FPS with lower resolution  
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # self.cap.set(cv2.CAP_PROP_FPS, 90)
        
        # Force MJPEG format for higher FPS (most webcams support this)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        
        # Reduce buffering
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Check what actually got set
        actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        print(f"📹 Camera settings:")
        print(f"   Resolution: {actual_width}x{actual_height}")
        print(f"   FPS: {actual_fps}")
        
        self.br = CvBridge()
        self.get_logger().info('✅ Webcam publisher started!')

    def timer_callback(self):
        # Capture frame
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
                    self.get_logger().info(f'📤 Publishing at {fps*2:.1f} FPS')
                    self.frame_count = 0
                    self.last_time = current_time
                    
            except Exception as e:
                self.get_logger().error(f'❌ Error: {str(e)}')
        else:
            self.get_logger().warning('⚠️ Failed to capture frame')

def main():
    print("Initializing ROS 2...")
    rclpy.init()
    
    try:
        image_publisher = ImagePublisher()
        print("Node created successfully!")
        print("Spinning... (Press Ctrl+C to stop)")
        rclpy.spin(image_publisher)
        
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🧹 Cleaning up...")
        if 'image_publisher' in locals():
            image_publisher.destroy_node()
        rclpy.shutdown()
        print("✅ Shutdown complete")

if __name__ == '__main__':
    main()