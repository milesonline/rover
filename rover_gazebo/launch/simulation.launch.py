import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # -----------------------------
    # Robot description
    # -----------------------------

    robot_description = ParameterValue(
        Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('robot_description'),
                'robot_urdf_description',
                'robot_body.xacro'
            ])
        ]),
        value_type=str
    )


    # -----------------------------
    # Planet world
    # -----------------------------

    world = PathJoinSubstitution([
        FindPackageShare('rover_gazebo'),
        'worlds',
        'planet.world'
    ])


    # -----------------------------
    # Gazebo
    # -----------------------------

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('ros_gz_sim'),
            '/launch/gz_sim.launch.py'
        ]),
        launch_arguments={
            'gz_args': ['-r ', world]
        }.items()
    )


    # -----------------------------
    # Robot State Publisher
    # -----------------------------

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description}
        ]
    )


    # -----------------------------
    # Spawn rover
    # -----------------------------

    spawn_rover = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'rover',
            '-z', '0.5'
        ],
        output='screen'
    )


    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        spawn_rover

    ])