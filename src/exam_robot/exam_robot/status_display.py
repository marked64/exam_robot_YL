#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class StatusDisplay(Node):

    def __init__(self):
        super().__init__('status_display')
        
        self.current_distance = 3.0  # текущее расстояние
        self.current_battery = 100.0  # текущий уровень батареи (начальное значение)
        
        self.status_publisher = self.create_publisher(
            String,
            '/robot_status',
            10
        )
        
        self.distance_sub = self.create_subscription(
            Float32, 
            '/distance',
            self.callback_distance,
            10
        )
        
        self.battery_sub = self.create_subscription(
            Float32, 
            '/battery_level',
            self.callback_battery,
            10
        )
        
        self.timer = self.create_timer(0.5, self.publish_status)
    
    def callback_distance(self, msg):
        self.current_distance = msg.data
        # Отладка (опционально)
        # self.get_logger().debug(f'Distance updated: {self.current_distance}')
    
    def callback_battery(self, msg):
        self.current_battery = msg.data
        # Отладка (опционально)
        # self.get_logger().debug(f'Battery updated: {self.current_battery}')
    
    def publish_status(self):
        msg = String()
        
        
        if self.current_battery >= 20 and self.current_distance >= 1:
            msg.data = "ALL OK"
        elif self.current_battery < 20 and self.current_battery >= 10 and self.current_distance >= 1:
            msg.data = "WARNING: Low battery"
        elif self.current_distance < 1 and self.current_distance >= 0.7 and self.current_battery >= 20:
            msg.data = "WARNING: Obstacle close"
        elif self.current_battery < 10 or self.current_distance < 0.7:
            msg.data = "CRITICAL"
        
        self.status_publisher.publish(msg)
        
        self.get_logger().info(msg.data)



def main(args = None):
      rclpy.init(args = args)
      node = StatusDisplay()
      rclpy.spin(node)
      rclpy.shutdown()


if __name__ == '__main__':
      main()
