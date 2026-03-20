#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool  # Импортируем тип сообщения


class RobotTemperatureStation(Node):
    """
    Узел-издатель, который публикует temperature робота.
    """

    def __init__(self):
        super().__init__('temperature_sensor')
        # Начальные параметры
        self.temperature = 30 # температура
        self.is_robot_moving = False # движется ли робот
        self.temperature_publisher = self.create_publisher(Float32,  # тип сообщения
            '/temperature',  # имя топика
            10  # размер очереди
        )

        self.motor_subscriber = self.create_subscription(
            Bool,
            '/motor_state',
            self.motor_state_callback,
            10
        )
        self.timer = self.create_timer(2.0, self.update_temp)
        self.get_logger().info('temperature monitoring started')

    def motor_state_callback(self, msg):
        """
        Получаем информацию о состоянии моторов.
        """
        self.is_robot_moving = msg.data
        state = "MOVING" if self.is_robot_moving else "IDLE"
    def update_temp(self):
        if self.temperature <= 26:
            self.temperature = 26
        elif self.temperature >=81:
            self.temperature = 81
        
        if self.is_robot_moving:
            self.temperature_change = 2
        else:
            self.temperature_change = -1
        
        self.temperature += self.temperature_change

        msg = Float32()
        msg.data = float(self.temperature)
        self.temperature_publisher.publish(msg)
        if self.temperature > 70:
            self.get_logger().warn(f'Warning, evacuate the facility immediately. Robot temperature {self.temperature}')
        elif self.temperature <=70:
            self.get_logger().info(f'Robot temperature {self.temperature}')


def main(args=None):
    rclpy.init(args=args)
    node = RobotTemperatureStation()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
