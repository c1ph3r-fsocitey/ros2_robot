# your_robot_launch.py

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    urdf_path = LaunchConfiguration('urdf_path', default='my_robot_description/urdf/my_robot.urdf.xacro')
    rviz_config_path = LaunchConfiguration('rviz_config_path', default='my_robot_description/rviz/urdf_config.rviz')
    joint_state_controller_path = get_package_share_directory('my_robot_description') + '/config/joint_state_controller.yaml'

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': f'$(xacro {urdf_path})'}],
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
        ),

        Node(
            package='controller_manager',
            executable='ros2_control_node',
            name='ros2_control_node',
            output='screen',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'robot_description': f'$(xacro {urdf_path})'},
            ],
        ),

        Node(
            package='ros2_controllers',
            executable='controller_manager',
            name='controller_manager',
            output='screen',
            arguments=['--ros-args', '--param', 'use_sim_time', LaunchConfiguration('use_sim_time')],
        ),

        Node(
            package='ros2_controllers',
            executable='ros2_control_parameter_server',
            name='ros2_control_parameter_server',
            output='screen',
            parameters=[{'controller_manager_ns': 'front_wheels_controller'}],
        ),

        Node(
            package='ros2_controllers',
            executable='spawner',
            name='joint_state_controller_spawner',
            output='screen',
            arguments=['joint_state_controller'],
        ),
    ])
