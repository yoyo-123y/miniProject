
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='joy',
            executable='game_controller_node',
            name='joystick'
        ),

        Node(
            package='my_robot',
            executable='send',
            name='controller_sender',
            output='screen'
        ),

        Node(
            package='my_robot',
            executable='receive',
            name='udp_sender',
            output='screen'
        )
    ])
