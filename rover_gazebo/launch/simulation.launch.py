import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit


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
            {'robot_description': robot_description},
            {'use_sim_time': True}
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

    # blah
    #spawn joint state and driver controllers

    joint_state_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
        ],
        output='screen',
    )

    drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'drive_controller',
            '--controller-manager',
            '/controller_manager',
        ],
        output='screen',
    )

    start_controllers = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_rover,
            on_exit=[
                joint_state_spawner,
                drive_controller_spawner,
            ],
        )
    )

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen',
    )

    lidar_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/lidar/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
        ],
        output='screen',
    )

    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0',
            '--y', '0',
            '--z', '0',
            '--frame-id', 'lidar_link',
            '--child-frame-id', 'rover/base_link/rover_lidar'
        ],
        output='screen'
    )


    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        spawn_rover,

        start_controllers,

        clock_bridge,

        lidar_bridge,

        lidar_tf,

    ])