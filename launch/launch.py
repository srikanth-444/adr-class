from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='stopsign_pkg',
            executable='stopsign',
            name='stop',
            output='screen'
           
        ),
        Node(
            package='driver_pkg',
            executable='drive',
            name='driver',
            output='screen'
        ),   
        Node(
            package='ekf_slam',
            executable='ekf_slam',
            name='slam',
            output='screen'
        )
    ])
