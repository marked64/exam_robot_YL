#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist


class RobotController(Node):

      def __init__(self):
            super().__init__('robot_controller')
            self.linear_x = 0.0
            self.angular_z = 0.0
            self.status = "ALL OK"

            self.control_publisher = self.create_publisher(
                  Twist,
                  '/cmd_vel',
                  10
            )
            self.status_subscriber = self.create_subscription(
                String, 
                '/robot_status',
                self.callback_news,
                10
            )


            self.timer = self.create_timer(0.1, self.publish_velocity)


      def publish_velocity(self):
            msg = Twist()
            msg.linear.x = self.linear_x
            msg.angular.z = self.angular_z
            self.control_publisher.publish(msg)
            
        
      def callback_news(self, msg):
            self.status = msg.data
            if self.status == "ALL OK":
                self.linear_x = 0.3
                self.angular_z = 0
            elif self.status == "WARNING: Low battery":
                self.linear_x = 0.1
                self.angular_z = 0
            elif self.status == "WARNING: Obstacle close":
                self.linear_x = 0
                self.angular_z = 0.5
            elif self.status == "CRITICAL":
                self.linear_x = 0
                self.angular_z = 0
            self.get_logger().info(self.status)
            self.get_logger().info(f'Current state: linear_x = {self.linear_x}, angular_z = {self.angular_z}')

        




def main(args = None):
      rclpy.init(args = args)
      node = RobotController()
      rclpy.spin(node)
      rclpy.shutdown()


if __name__ == '__main__':
      main()
