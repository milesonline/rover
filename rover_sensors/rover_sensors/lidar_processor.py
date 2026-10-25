import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

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


    def scan_callback(self, msg: LaserScan):
        """
        Called every time a scan comes in
        """
        # get LiDAR measurements
        ranges = msg.ranges


        nearest_obstacle= float('inf')
        nearest_index = -1
        #Set obstacle threshold
        obstacle_threshold = 2.0

        for index, num in enumerate(ranges):
            #Ignore invalid measurements
            if math.isfinite(num) and msg.range_min <= num <= msg.range_max:
                if num < nearest_obstacle:
                    nearest_obstacle = num
                    nearest_index = index

        #process result after checking the whole scan
        if nearest_index != -1:
            # Calculate the angle in radians
            angle = msg.angle_min + (nearest_index * msg.angle_increment)
            # Convert radians to degrees
            angle_degrees = math.degrees(angle)

            # Report the nearest return
            self.get_logger().info(
                f'Nearest return: {nearest_obstacle:.2f} metres '
                f'at index {nearest_index}, '
                f'angle {angle_degrees: .1f} degrees'
            )

            #warn if return is within the threshold
            if nearest_obstacle < obstacle_threshold:
                self.get_logger().warn(
                    f'Nearest return within threshold: '
                    f'{nearest_obstacle:.2f} metres'
                )


def main(args=None):
    rclpy.init(args=args)
    node = LidarProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()