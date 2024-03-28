import rclpy
from rclpy.node import Node
import numpy as np

from sensor_msgs.msg import laser_scan 

class Service_Node(Node):
    def __init__(self):
        super().__init__('service_node')
        self.subcriber= self.create_subscription(laser_scan, '/rplidar_ros/scan',self.listen,10,)


    def listen(self, msg):
        
        lidar_data = np.array(msg) 
        print(lidar_data)
       

def main(args=None):
    rclpy.init(args=args)

    service_node = Service_Node()


    
    rclpy.spin(service_node)
    service_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
