from setuptools import find_packages, setup

package_name = 'robot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/display.launch.py']),
        ('share/' + package_name + '/rviz' , ['rviz/rover.rviz']),
        ('share/' + package_name + '/robot_urdf_description',
         [
             'robot_urdf_description/robot_body.xacro',
             'robot_urdf_description/chassis.xacro',
             'robot_urdf_description/wheels.xacro',
             'robot_urdf_description/sensors.xacro',
         ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sam_i',
    maintainer_email='olatilewa.ishola.2021@mumail.ie',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
