from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

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

    #Rviz config
    rviz_config = PathJoinSubstitution([
        FindPackageShare('robot_description'),
        'rviz',
        'rover.rviz'
    ])

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config]
        )
    ])


