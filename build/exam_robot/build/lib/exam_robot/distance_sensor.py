#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class DistanceSensor(Node):

      def __init__(self):
            super().__init__('distance_sensor')

            self.distance = 3.0

            self.distance_publisher = self.create_publisher(
                  Float32,
                  '/distance',
                  10
            )
            self.cmd_vel = self.create_subscription(
                Twist, 
                '/cmd_vel',
                self.callback_news,
                10
            )


            self.timer = self.create_timer(0.2, self.publish_battery_level)


      def publish_battery_level(self):
            msg = Float32()
            if self.linear_x > 0:
                self.distance -= 0.2
            elif self.linear_x < 0:
                self.distance += 0.2
            elif self.linear_x == 0:
                self.distance = 3.0
            self.distance = max(0.5, self.distance)
            self.distance = min(3.0, self.distance)
            msg.data = self.distance
            self.distance_publisher.publish(msg)
            
        
      def callback_news(self, msg):
            self.linear_x = msg.linear.x

        




def main(args = None):
      rclpy.init(args = args)
      node = DistanceSensor()
      rclpy.spin(node)
      rclpy.shutdown()


if __name__ == '__main__':
      main()
