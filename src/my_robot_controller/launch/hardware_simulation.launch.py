from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # STM32 Bridge (имитация микроконтроллера)
        Node(
        package='my_robot_controller',
        executable='stm32_bridge',
        name='stm32_bridge',
        output='screen',
        prefix='xterm -e' # отдельное окно
        ),

        # Датчики (управляются STM32)
        Node(
        package='my_robot_controller',
        executable='imu_simulator',
        name='imu_simulator',
        output='screen'
        ),
        Node(
        package='my_robot_controller',
        executable='encoder_simulator',
        name='encoder_simulator',
        output='screen'
        ),
        Node(
        package='my_robot_controller',
        executable='lidar_simulator',
        name='lidar_simulator',
        output='screen'
        ),

        # Обработка данных (на RPI5)
        Node(
        package='my_robot_controller',
        executable='imu_reader',
        name='imu_reader',
        output='screen'
        ),
        Node(
        package='my_robot_controller',
        executable='wheel_odometry',
        name='wheel_odometry',
        output='screen'
        ),

        # Мониторинг (из прошлого занятия)
        Node(
        package='my_robot_controller',
        executable='battery_node',
        name='battery_node',
        output='screen'
        ),
        Node(
        package='my_robot_controller',
        executable='system_monitor',
        name='system_monitor',
        output='screen'
        ),
        ])
