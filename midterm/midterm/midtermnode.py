import rclpy
from rclpy.node import Node
import numpy as np
    
from deepracer_interfaces_pkg.msg import EvoSensorMsg
from deepracer_interfaces_pkg.srv import LidarConfigSrv
    
    
class Distance_Calculator(Node):

    def __init__(self):
        super().__init__('distance_calculator')
        self.subcriber= self.create_subscription(EvoSensorMsg, '/sensor_fusion_pkg/sensor_msg',self.listen,10,)
        self.client=self.create_client(LidarConfigSrv,"/sensor_fusion_pkg/configure_lidar")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = LidarConfigSrv.Request()
        
       
    def send_request(self,):
        self.req.use_lidar=True
        self.req.min_angle= -179.0
        self.req.max_angle= 179.0
        self.req.num_values=600
        self.req.min_distance=0.15
        self.req.max_distance=1.0
        self.req.clipping_distance=1.0
        self.req.num_sectors=60
        self.req.preprocess_type=0
        self.future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()                      

    def listen(self, msg):
        
        lidar_data = np.array(msg.lidar_data) 
        distance_matrix=np.array([])
        
        distance_matrix=np.concatenate((lidar_data[1:100],lidar_data[-100:]))

        least_distance=distance_matrix[np.argmax(distance_matrix)]
       
        
        print(least_distance)
   

       

           


def main(args=None):
    rclpy.init(args=args)

    distance_calculator = Distance_Calculator()


    res=distance_calculator.send_request()
    if (res.error==1):
        print("lidar config wrong you idiot")
        rclpy.shutdown()
    rclpy.spin(distance_calculator)
    distance_calculator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
