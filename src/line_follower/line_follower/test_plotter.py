import rclpy
from rclpy.node import Node
from line_interfaces.msg import LineError
from geometry_msgs.msg import Twist
import signal

class PIDControllerNode(Node):
    def __init__(self):
        super().__init__('pid_controller_node')

        self.error_subscriber = self.create_subscription(
            LineError, '/line/error_position', self.error_callback, 10)
        self.error_subscriber

        self.robot_move_subscriber = self.create_subscription(
            Twist, '/cmd_vel', self.vel_callback, 10)
        self.robot_move_subscriber
        
        # PID constants
        self.Kp = 0.015
        self.Ki = 0.0
        self.Kd = 0.0

        # Initialize PID control variables
        self.prev_error = 0
        self.integral = 0

        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown_handler)

        self.get_logger().info(f"hello world")

    def error_callback(self, msg):
        self.get_logger().info(f"Receviev sub")
        current_error = msg.current_error
        angular_velocity = self.calculate_angular_velocity(current_error)
        self.publish_velocity(angular_velocity)

    def calculate_angular_velocity(self, error):
        self.integral += error
        derivative = error - self.prev_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # Update previous error
        self.prev_error = error
        self.get_logger().info(f"Publishing error msg: {output}")
        return output

    def publish_velocity(self, angular_velocity):
        # Fix the base velocity in linear (for example, 0.1 m/s in x and y axes)
        linear_velocity = 1.0

        # Create Twist message
        twist = Twist()
        twist.linear.x = linear_velocity
        twist.angular.z = -angular_velocity

        # Publish Twist message
        self.velocity_publisher.publish(twist)

    def stop_robot(self):
        # Create Twist message with zero velocities
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.angular.z = 0.0
        self.velocity_publisher.publish(twist)

    def shutdown_handler(self, signum, frame):
        self.get_logger().info('Shutting down...')
        # Stop the robot before destroying the node
        self.stop_robot()
        self.destroy_node()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    pid_controller_node = PIDControllerNode()
    rclpy.spin(pid_controller_node)
    pid_controller_node.stop_robot()  # Stop the robot before shutting down
    pid_controller_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
