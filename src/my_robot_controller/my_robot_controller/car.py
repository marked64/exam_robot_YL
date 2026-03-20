#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Car(Node):
    """
    Узел-подписчик, который получает новости робота.
    """

    def __init__(self):
        super().__init__('smartphone')

        # Создаём Subscriber
        self.subscriber_ = self.create_subscription(
            String,  # тип сообщения
            '/traffic_light',  # имя топика
            self.callback_news,  # функция обработки
            10  # размер очереди
        )

    def callback_news(self, msg):
        """
        Эта функция вызывается при получении каждого сообщения
        """
        self.msg_data = msg.data
        if self.msg_data == 'RED':
            self.get_logger().info('Остановка!')
        elif self.msg_data == 'YELLOW':
            self.get_logger().info('Замедляюсь...')
        elif self.msg_data == 'GREEN':
            self.get_logger().info('Еду!')


def main(args=None):
    rclpy.init(args=args)
    node = Car()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
