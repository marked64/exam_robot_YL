#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class StatusDisplay(Node):

      def __init__(self):
            super().__init__('distance_sensor')

            self.distance = 3.0

            self.distance_publisher = self.create_publisher(
                  String,
                  '/robot_status',
                  10
            )
            self.distance = self.create_subscription(
                Float32, 
                '/distance',
                self.callback_distance,
                10
            )
            self.battery_level = self.create_subscription(
                Float32, 
                '/battery_level',
                self.callback_battery,
                10
            )


            self.timer = self.create_timer(0.5, self.publish_status)


      def callback_distance(self, msg):
        self.distance = msg.data


      def callback_battery(self, msg):
        self.battery = msg.data


      def publish_status(self):
        msg = String()
        if self.battery >= 20 and self.distance >= 1:
            msg.data = "ALL OK"
        elif self.battery < 20 and self.distance >= 1:
            msg.data = "WARNING: Low battery"
        elif self.distance < 1 and self.battery >= 20:
            msg.data = "WARNING: Obstacle close"
        elif self.battery < 10 or self.distance < 0.7:
            msg.data = "CRITICAL"
        
        self.distance_publisher.publish(msg)
        self.get_logger.info(msg)

        




def main(args = None):
      rclpy.init(args = args)
      node = StatusDisplay()
      rclpy.spin(node)
      rclpy.shutdown()


if __name__ == '__main__':
      main()
