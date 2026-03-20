#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
import math
import random

class ToFSimulator(Node):
    """
    Симулятор двух ToF датчиков VL52L0X (левый и правый).
    
    Характеристики:
    - Диапазон: 0.03 - 2.0 метра
    - Частота: 50 Hz
    - Топики: /tof/left, /tof/right
    - Тип: sensor_msgs/msg/Range
    """
    
    def __init__(self):
        super().__init__('tof_simulator')
        
        # Параметры датчиков VL52L0X
        self.min_range = 0.03       # минимальная дальность (метры)
        self.max_range = 2.0        # максимальная дальность (метры)
        self.fov = 0.5236           # поле зрения (30 градусов в радианах)
        self.frequency = 50          # частота публикации (Гц)
        
        # Параметры симуляции движения
        self.robot_x = 0.0           # позиция робота по X
        self.robot_y = 0.0           # позиция робота по Y
        self.robot_theta = 0.0       # угол поворота робота
        
        # Препятствия в пространстве (x, y, радиус)
        self.obstacles = [
            {'x': 1.5, 'y': 0.0, 'radius': 0.3},   # препятствие прямо
            {'x': 2.5, 'y': 0.8, 'radius': 0.4},   # препятствие справа
            {'x': 2.0, 'y': -0.7, 'radius': 0.35}, # препятствие слева
            {'x': 3.5, 'y': -0.3, 'radius': 0.5},  # дальнее препятствие
            {'x': 0.8, 'y': 1.2, 'radius': 0.25},  # препятствие слева-сбоку
            {'x': 0.9, 'y': -1.1, 'radius': 0.3},  # препятствие справа-сбоку
        ]
        
        # Создаем издатели для левого и правого датчиков
        self.left_pub = self.create_publisher(Range, '/tof/left', 10)
        self.right_pub = self.create_publisher(Range, '/tof/right', 10)
        
        # Подписываемся на команды скорости для симуляции движения
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # Таймер для публикации данных с заданной частотой
        self.timer_period = 1.0 / self.frequency
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.get_logger().info(
            f'ToF симулятор (VL52L0X) запущен\n'
            f'  Частота: {self.frequency} Hz\n'
            f'  Диапазон: {self.min_range} - {self.max_range} м\n'
            f'  Топики: /tof/left, /tof/right'
        )
    
    def cmd_vel_callback(self, msg):
        """
        Обновляет позицию робота на основе команд скорости.
        """
        # Получаем линейную и угловую скорость
        vx = msg.linear.x
        omega = msg.angular.z
        
        # Временной шаг (предполагаем, что callback вызывается каждые 50 мс)
        dt = 0.05
        
        # Обновляем позицию (простая кинематическая модель)
        self.robot_x += vx * math.cos(self.robot_theta) * dt
        self.robot_y += vx * math.sin(self.robot_theta) * dt
        self.robot_theta += omega * dt
        
        # Нормализуем угол
        self.robot_theta = math.atan2(math.sin(self.robot_theta), 
                                      math.cos(self.robot_theta))
    
    def create_range_message(self, sensor_id):
        """
        Создает сообщение Range для указанного датчика.
        """
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f'tof_{sensor_id}_link'
        
        # Для ToF датчиков используем инфракрасный тип
        msg.radiation_type = Range.INFRARED
        
        msg.field_of_view = self.fov
        msg.min_range = self.min_range
        msg.max_range = self.max_range
        
        return msg
    
    def calculate_distance(self, sensor_offset_x, sensor_offset_y, sensor_angle_offset):
        """
        Вычисляет расстояние до ближайшего препятствия для конкретного датчика.
        
        Args:
            sensor_offset_x: смещение датчика по X относительно центра робота
            sensor_offset_y: смещение датчика по Y относительно центра робота
            sensor_angle_offset: угол отклонения датчика от направления робота
            
        Returns:
            float: измеренное расстояние в метрах
        """
        # Позиция датчика в глобальной системе координат
        sensor_x = self.robot_x + sensor_offset_x * math.cos(self.robot_theta) - sensor_offset_y * math.sin(self.robot_theta)
        sensor_y = self.robot_y + sensor_offset_x * math.sin(self.robot_theta) + sensor_offset_y * math.cos(self.robot_theta)
        
        # Направление луча датчика (с учетом поворота робота)
        ray_angle = self.robot_theta + sensor_angle_offset
        ray_direction = (math.cos(ray_angle), math.sin(ray_angle))
        
        min_dist = self.max_range
        
        for obs in self.obstacles:
            # Вектор от датчика к препятствию
            dx = obs['x'] - sensor_x
            dy = obs['y'] - sensor_y
            
            # Расстояние от датчика до центра препятствия
            dist_to_obs_center = math.sqrt(dx*dx + dy*dy)
            
            # Угол до препятствия
            angle_to_obs = math.atan2(dy, dx)
            
            # Проверяем, находится ли препятствие в поле зрения датчика
            angle_diff = abs(angle_to_obs - ray_angle)
            angle_diff = min(angle_diff, 2*math.pi - angle_diff)
            
            if angle_diff < self.fov / 2:
                # Препятствие в поле зрения
                # Проекция на направление луча
                t = dx * ray_direction[0] + dy * ray_direction[1]
                
                if t > 0:  # препятствие впереди по лучу
                    # Расстояние до поверхности препятствия
                    # (используем теорему Пифагора)
                    dist_to_surface = math.sqrt(dist_to_obs_center**2 - (dist_to_obs_center * math.sin(angle_diff))**2)
                    dist_to_surface = max(0, dist_to_surface - obs['radius'])
                    
                    if dist_to_surface < min_dist:
                        min_dist = dist_to_surface
        
        # Если препятствий нет, возвращаем случайное значение
        if min_dist >= self.max_range:
            # Случайное расстояние, но чаще ближе к максимальному
            min_dist = self.max_range - random.uniform(0, 0.5)
        
        # Добавляем небольшой шум (±1 см)
        noise = random.gauss(0, 0.01)
        min_dist += noise
        
        # Ограничиваем значения в пределах дальности
        return max(self.min_range, min(self.max_range, min_dist))
    
    def timer_callback(self):
        """Публикует данные с обоих ToF датчиков."""
        
        # Левый датчик (смещен влево и смотрит прямо)
        # При повороте налево левый датчик будет показывать меньшее расстояние
        left_dist = self.calculate_distance(
            sensor_offset_x=0.1,    # впереди робота
            sensor_offset_y=0.08,   # слева от центра
            sensor_angle_offset=0.0  # смотрит прямо
        )
        
        # Правый датчик (смещен вправо и смотрит прямо)
        # При повороте направо правый датчик будет показывать меньшее расстояние
        right_dist = self.calculate_distance(
            sensor_offset_x=0.1,    # впереди робота
            sensor_offset_y=-0.08,  # справа от центра
            sensor_angle_offset=0.0  # смотрит прямо
        )
        
        # Публикуем левый датчик
        left_msg = self.create_range_message('left')
        left_msg.range = left_dist
        self.left_pub.publish(left_msg)
        
        # Публикуем правый датчик
        right_msg = self.create_range_message('right')
        right_msg.range = right_dist
        self.right_pub.publish(right_msg)
        
        # Логируем каждое 50-е сообщение (раз в секунду при 50 Гц)
        if not hasattr(self, 'counter'):
            self.counter = 0
        self.counter += 1
        
        if self.counter % 50 == 0:
            # Показываем асимметрию при повороте
            asymmetry = abs(left_dist - right_dist)
            direction = "прямо"
            if left_dist < right_dist - 0.1:
                direction = "поворот НАЛЕВО (объект слева ближе)"
            elif right_dist < left_dist - 0.1:
                direction = "поворот НАПРАВО (объект справа ближе)"
            
            self.get_logger().info(
                f'Левый: {left_dist:.3f} м | Правый: {right_dist:.3f} м | '
                f'Асимметрия: {asymmetry:.3f} м | {direction}'
            )


class SimpleToFSimulator(ToFSimulator):
    """
    Упрощенная версия для тестирования без сложной геометрии.
    """
    
    def calculate_distance(self, sensor_offset_x, sensor_offset_y, sensor_angle_offset):
        """
        Упрощенная модель: расстояние зависит от скорости и поворота.
        """
        # Базовая дистанция (уменьшается при движении вперед)
        base_dist = 1.5
        
        # Получаем последнюю команду скорости (имитируем)
        # Для демонстрации используем случайные значения
        vx = random.uniform(-0.2, 0.5)  # скорость вперед/назад
        omega = random.uniform(-0.5, 0.5)  # угловая скорость
        
        # При движении вперед расстояние уменьшается
        if vx > 0:
            base_dist -= vx * 2.0
        
        # Асимметрия при повороте
        if omega > 0.1:  # поворот налево
            # Левый датчик видит препятствие ближе
            if sensor_offset_y > 0:  # левый датчик
                base_dist -= omega * 1.5
            else:  # правый датчик
                base_dist += omega * 0.5
        elif omega < -0.1:  # поворот направо
            # Правый датчик видит препятствие ближе
            if sensor_offset_y < 0:  # правый датчик
                base_dist -= abs(omega) * 1.5
            else:  # левый датчик
                base_dist += abs(omega) * 0.5
        
        # Добавляем шум
        base_dist += random.gauss(0, 0.02)
        
        # Ограничиваем диапазон
        return max(self.min_range, min(self.max_range, base_dist))


def main(args=None):
    rclpy.init(args=args)
    
    # Используйте ToFSimulator для полной версии с препятствиями
    # или SimpleToFSimulator для упрощенной версии
    node = ToFSimulator()
    # node = SimpleToFSimulator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('ToF симулятор остановлен')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
