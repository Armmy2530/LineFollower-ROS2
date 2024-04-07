import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import line_follower.image_process
 
class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_pub')
        
        self.publisher_ = self.create_publisher(Image, 'test_image', 10)
        # Create a VideoCapture object
        # The argument '0' gets the default webcam.
        self.img = cv2.imread('/root/armmyCameraRobot/armmyRobot/src/line_follower/data/test_data/1.png')
      
        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()
      
        # We will publish a message every 0.1 seconds
        timer_period = 0.1  # seconds
        
        # Create the timer
        self.timer = self.create_timer(timer_period, self.test_pub)
    
    def test_pub(self):
        self.publisher_.publish(self.br.cv2_to_imgmsg(self.img,encoding='rgb8'))
        self.get_logger().info('Publishing image')


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
