#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import json

class STM32Bridge(Node):
    """
    Имитация STM32 микроконтроллера.
    Принимает команды от RPI через "UART" и управляет датчикам
    """

    def __init__(self):
        super().__init__('stm32_bridge')

        # Subscriber на команды от RPI
        self.cmd_sub = self.create_subscription(
        Twist,
        '/cmd_vel',
        self.cmd_callback,
        10
        )

        # Publisher для статуса STM32
        self.status_pub = self.create_publisher(
        String,
        '/stm32/status',
        10
        )

        # Таймер для отправки телеметрии
        self.timer = self.create_timer(0.1, self.send_telemetr

        # Счетчики
        self.cmd_count = 0
        self.telemetry_count = 0

        self.get_logger().info('STM32 Bridge started')
        self.get_logger().info('Simulating STM32F405RG microcontroller')
        self.get_logger().info('UART communication: RPI5 ↔ STM32')

    def cmd_callback(self, msg):
        """
        Получили команду от Raspberry Pi (через "UART").
        """
        self.cmd_count += 1

        # В реальности STM32 получает байты через UART
        # и декодирует их в структуру команд

        self.get_logger().info(
            f'[STM32] RX from RPI: CMD_VEL #{self.cmd_count} | '
            f'linear={msg.linear.x:.2f} angular={msg.angular.z:.2f}'
        )

        # Здесь STM32 обновил бы PWM моторов
        # Наши симуляторы подписаны напрямую на /cmd_vel

    def send_telemetry(self):
        """
        Отправка телеметрии от STM32 к RPI (через "UART").
        """
        self.telemetry_count += 1

        # В реальности STM32 собирает данные со всех датчиков
        # и отправляет пакет через UART

        telemetry = {
        'packet_id': self.telemetry_count,
        'sensors_active': {
        'imu': True,
        'encoders': True,
        'lidar': True,
        'tof': True
        },
        'battery_voltage': 8.1, # вольт (2S Li-Po)
        'stm32_temp': 42.5 # °C
        }

        msg = String()
        msg.data = json.dumps(telemetry)
        self.status_pub.publish(msg)

        if self.telemetry_count % 10 == 0:
            self.get_logger().info(
                f'[STM32] TX to RPI: TELEMETRY #{self.telemetry_count} | '
                f'All sensors OK, Battery: {telemetry["battery_voltage"]}V'
            )

def main(args=None):
    rclpy.init(args=None)
    node = STM32Bridge()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
