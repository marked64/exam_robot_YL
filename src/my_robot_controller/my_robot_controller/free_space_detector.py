#!/usr/bin/env python3
"""
Узел для определения самого широкого свободного направления по данным лидара.
Адаптирован под ROS2, используя стиль кода из lidar_processor.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3
import math


class FreeSpaceDetector(Node):
    """
    Подписывается на /scan (sensor_msgs/LaserScan),
    находит самый широкий непрерывный сектор без препятствий
    и публикует результат в /free_direction (geometry_msgs/Vector3).
    """

    def __init__(self):
        super().__init__('free_space_detector')

        # Параметры
        self.declare_parameter('min_distance', 0.5)   # минимальное расстояние до препятствия (м)
        self.min_distance = self.get_parameter('min_distance').value

        # Подписчик на данные лидара
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Издатель результата
        self.free_dir_pub = self.create_publisher(
            Vector3,
            '/free_direction',
            10
        )

        self.get_logger().info(
            f'FreeSpaceDetector инициализирован: min_distance = {self.min_distance:.2f} м'
        )

    def scan_callback(self, msg: LaserScan):
        """
        Обработчик сообщения LaserScan.
        Анализирует дальности и находит самый широкий свободный сектор.
        """
        # Извлекаем данные из сообщения
        ranges = msg.ranges
        angle_min = msg.angle_min
        angle_inc = msg.angle_increment
        n = len(ranges)

        # Переменные для хранения лучшего сектора
        best_width = 0.0          # ширина лучшего сектора (рад)
        best_angle = 0.0          # угол центра лучшего сектора (рад)
        best_min_dist = 0.0       # минимальное расстояние в лучшем секторе (м)

        # Состояние текущего свободного сектора
        in_sector = False
        sector_start_idx = 0
        sector_min_dist = float('inf')
        sector_end_idx = 0

        for i in range(n):
            d = ranges[i]

            # Определяем, является ли луч свободным (расстояние больше порога)
            free = False
            if math.isnan(d):          # NaN считается свободным
                free = True
            elif math.isinf(d):        # Inf (бесконечность) считается свободным
                free = True
            elif d >= self.min_distance:
                free = True

            if free:
                if not in_sector:
                    # Начинаем новый сектор
                    in_sector = True
                    sector_start_idx = i
                    # Инициализируем минимальное расстояние
                    if not math.isnan(d) and not math.isinf(d):
                        sector_min_dist = d
                    else:
                        sector_min_dist = float('inf')
                else:
                    # Обновляем минимальное расстояние в текущем секторе
                    if not math.isnan(d) and not math.isinf(d) and d < sector_min_dist:
                        sector_min_dist = d
            else:
                # Встретили препятствие: закрываем текущий сектор, если он был открыт
                if in_sector:
                    sector_end_idx = i - 1
                    start_angle = angle_min + sector_start_idx * angle_inc
                    end_angle = angle_min + sector_end_idx * angle_inc
                    width = end_angle - start_angle
                    center_angle = (start_angle + end_angle) / 2.0

                    if width > best_width:
                        best_width = width
                        best_angle = center_angle
                        best_min_dist = sector_min_dist

                    in_sector = False
                    sector_min_dist = float('inf')

        # Если после обработки всех лучей остался открытый сектор, закрываем его
        if in_sector:
            sector_end_idx = n - 1
            start_angle = angle_min + sector_start_idx * angle_inc
            end_angle = angle_min + sector_end_idx * angle_inc
            width = end_angle - start_angle
            center_angle = (start_angle + end_angle) / 2.0

            if width > best_width:
                best_width = width
                best_angle = center_angle
                best_min_dist = sector_min_dist

        # Формируем и публикуем сообщение Vector3
        msg_out = Vector3()
        msg_out.x = best_angle
        msg_out.y = best_min_dist
        msg_out.z = best_width
        self.free_dir_pub.publish(msg_out)

        # Отладочный вывод (уровень DEBUG можно настроить через rqt_logger_level)
        self.get_logger().debug(
            f'Свободное направление: угол = {best_angle:.2f} рад, '
            f'мин. расстояние = {best_min_dist:.2f} м, ширина = {best_width:.2f} рад'
        )


def main(args=None):
    rclpy.init(args=args)
    node = FreeSpaceDetector()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()