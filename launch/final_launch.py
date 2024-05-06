from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='driver_pkg',
            executable='drive',
        ),
        Node(
            package='ekf_slam',
            executable='ekf_slam',
        ),
        Node(
            package='stop_sign',
            executable='stopsign',
           
        )
    ])