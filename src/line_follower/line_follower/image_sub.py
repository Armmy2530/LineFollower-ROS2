# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
  
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from geometry_msgs.msg      import Point
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import line_follower.image_process as line_imp
from line_interfaces.msg import LineError
 
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')

    self.image_pub = self.create_publisher(Image, 'camera/line2p_image', 10)
    self.line_pub = self.create_publisher(LineError, 'line/error_position' ,10)

    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image, 
      'camera/image_raw', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
    
    # Line follower variable
    self.last_error = -1
    self.found_line = False
   
  def listener_callback(self, data):
    """
    Callback function.
    """
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)
    
    h, w , _ = current_frame.shape
    centerline_point = line_imp.find_point(current_frame,[400])
    if(centerline_point[0][0] != -1):
      centerline_draw_img = line_imp.drawimg_point(current_frame , centerline_point)
      error_fromcenter = centerline_point[0][2] - (w/2)
      self.last_error = error_fromcenter
      self.found_line = True
    else:
      centerline_draw_img = current_frame
      error_fromcenter = -1.0
      self.found_line = False

    # centerline_draw_img = line_imp.draw_centerline(current_frame)

    img_pub = self.br.cv2_to_imgmsg(centerline_draw_img,encoding='rgb8')
    img_pub.header = data.header

    line_error = LineError() 
    line_error.current_error = error_fromcenter
    line_error.last_error = self.last_error
    line_error.line_found = self.found_line
    self.get_logger().info(f"Publishing error msg: {self.found_line} {error_fromcenter} {self.last_error}")

    self.image_pub.publish(img_pub)
    self.line_pub.publish(line_error)
  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()