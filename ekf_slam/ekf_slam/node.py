import rclpy
from rclpy.node import Node
import numpy as np

from sensor_msgs.msg import LaserScan

class Service_Node(Node):
    def __init__(self):
        super().__init__('service_node')
        self.subcriber= self.create_subscription(LaserScan, '/rplidar_ros/scan',self.listen,10,)


    def listen(self, msg):
        
        lidar_data = msg 
        min_angle=lidar_data.angle_min
        max_angle=lidar_data.angle_max
        angle_increment=lidar_data.angle_increment

        
        distance=np.array(lidar_data.ranges)
        samples=distance.size
        angle=np.linspace(min_angle,max_angle,samples)

        for i in range(samples):
            if distance[i]==float('inf'):
                distance[i]=8

        map_space=np.squeeze(np.column_stack((angle,distance)),axis=1)

        print(map_space)

def main(args=None):
    rclpy.init(args=args)

    service_node = Service_Node()


    
    rclpy.spin(service_node)
    service_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
