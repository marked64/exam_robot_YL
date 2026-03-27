from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.urdf'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='aternos.me64@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['my_first_node = my_robot_controller.my_first_node:main',
         'my_second_node = my_robot_controller.my_second_node:main',
         'robot_news_station = my_robot_controller.robot_news_file:main',
         'smartphone = my_robot_controller.smartphone:main',
         'temperature_sensor = my_robot_controller.temperature_sensor:main',
         'car = my_robot_controller.car:main',
         'traffic_light = my_robot_controller.traffic_light:main',
         'imu_simulator = my_robot_controller.imu_simulator:main',
         'imu_reader = my_robot_controller.imu_reader:main',
         'encoder_simulator = my_robot_controller.encoder_simulator:main',
         'wheel_odometry = my_robot_controller.wheel_odometry:main',
         'lidar_simulator = my_robot_controller.lidar_simulator:main',
         'stm32_bridge = my_robot_controller.stm32_bridge:main',
         'battery_node = my_robot_controller.battery_node:main',
         'system_monitor = my_robot_controller.system_monitor:main',
         'static_transform_publisher = my_robot_controller.static_transform_publisher:main',
         'sensor_fusion = my_robot_controller.sensor_fusion:main',
         'calibration_helper = my_robot_controller.calibration_helper:main',
         'lidar_processor = my_robot_controller.lidar_processor:main',
         'lidar_room_simulator = my_robot_controller.lidar_room_simulator:main',
         'free_space_detector = my_robot_controller.free_space_detector:main'
        ],
    },
)
