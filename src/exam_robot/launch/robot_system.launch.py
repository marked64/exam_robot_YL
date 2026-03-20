from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('exam_robot')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'exam_robot.urdf')
    with open(urdf_file, 'r') as file:
        robot_description = file.read()
    return LaunchDescription([
        Node(
            package='exam_robot',
            executable='battery_node',
            output='screen',
        ),
        Node(
            package='exam_robot',
            executable='distance_sensor',
            output='screen',
        ),
        Node(
            package='exam_robot',
            executable='robot_controller',
            output='screen',
        ),
        Node(
            package='exam_robot',
            executable='status_display',
            output='screen',
        ),
        # robot_state_publisher с URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),

        ])

