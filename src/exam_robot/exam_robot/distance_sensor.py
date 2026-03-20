#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class DistanceSensor(Node):

    def __init__(self):
        super().__init__('distance_sensor')
        self.linear_x = 0.0  # текущая линейная скорость
        self.distance = 3.0  # текущее расстояние до препятствия
        
        self.distance_publisher = self.create_publisher(
            Float32,
            '/distance',
            10
        )
        self.cmd_vel_sub = self.create_subscription(
            Twist, 
            '/cmd_vel',
            self.callback_cmd_vel,
            10
        )
        self.timer = self.create_timer(0.2, self.publish_distance)

    def publish_distance(self):
        """Публикует текущее расстояние до препятствия"""
        msg = Float32()

        if self.linear_x == 0:
            # Если стоим - расстояние максимальное
            self.distance = 3.0
        elif self.linear_x > 0:
            self.distance -= 0.2
        elif self.linear_x < 0:
            self.distance += 0.2
        if self.distance < 0.5:
            self.distance = 0.5
        if self.distance > 3.0:
            self.distance = 3.0

        msg.data = self.distance
        self.distance_publisher.publish(msg)
    
    def callback_cmd_vel(self, msg):
        self.linear_x = msg.linear.x


def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()