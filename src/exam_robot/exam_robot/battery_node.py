#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class BatteryNode(Node):

      def __init__(self):
            super().__init__('battery_node')

            self.battery_level = 100.0

            self.battery_publisher = self.create_publisher(
                  Float32,
                  '/battery_level',
                  10
            )

            self.timer = self.create_timer(1.0, self.publish_battery_level)


      def publish_battery_level(self):
            msg = Float32()
            msg.data = max(0.0, self.battery_level)
            self.battery_publisher.publish(msg)
            if self.battery_level % 10 == 0:
                  self.get_logger().info(f'Battery: {msg.data}%')
            self.battery_level -= 1


def main(args = None):
      rclpy.init(args = args)
      node = BatteryNode()
      rclpy.spin(node)
      rclpy.shutdown()


if __name__ == '__main__':
      main()
