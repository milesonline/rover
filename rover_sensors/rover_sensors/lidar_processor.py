import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import time

class LidarProcessor(Node):

    """
    Node that subscribes to lidar scan topic and detects obstacles within a chosen distance
    and reports their approximate direction
    """

    def __init__(self):
        super().__init__('lidar_processor')

        #Parameter which topic to lsiten to
        self.declare_parameter('scan_topic', '/lidar/scan')
        scan_topic = self.get_parameter('scan_topic').get_parameter_value().string_value

        # Subscribe to the scan
        self.scan_sub = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            10
        )

        # Publisher for Object detections
        self.detections_pub = self.create_publisher(
            LaserScan,
            '/rover_sensors/detections',
            10
        )

        self.get_logger().info(f"lidar detection node listening: {scan_topic}")
        self.get_logger().info(f"Publishing detections on: /rover_sensors/detections")

    def scan_callback(self, msg: LaserScan):
        """
        Called every time a scan comes in
        """
        pass   
