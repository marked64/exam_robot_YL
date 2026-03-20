#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Импортируем тип сообщения


class TrafficLight(Node):
    """
    Узел-издатель, который публикует новости робота.
    """

    def __init__(self):
        super().__init__('traffic_light')

        # Создаём Publisher
        self.publisher_ = self.create_publisher(
            String,  # тип сообщения
            '/traffic_light',  # имя топика
            10  # размер очереди
        )
        self.colors = ['RED', 'YELLOW', 'GREEN']
        self.counter = 0
    
        # Таймер для публикации каждые 0.5 секунды
        self.timer = self.create_timer(3, self.publish_color)

    def publish_color(self):

        """
        Функция публикации новостей.
        """
    
    
        # Создаём сообщение
        msg = String()
        msg.data = self.colors[self.counter]
    
        # Публикуем сообщение
        self.publisher_.publish(msg)
        self.counter += 1
        self.counter %= len(self.colors)


def main(args=None):
    rclpy.init(args=args)
    node = TrafficLight()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
