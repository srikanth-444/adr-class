import rclpy
from rclpy.node import Node
import numpy as np
    
from deepracer_interfaces_pkg.msg import EvoSensorMsg
from deepracer_interfaces_pkg.srv import LidarConfigSrv
from deepracer_interfaces_pkg.msg import ServoCtrlMsg
    
    
class Distance_Calculator(Node):

    def __init__(self):
        super().__init__('distance_calculator')
        self.subcriber= self.create_subscription(EvoSensorMsg, '/sensor_fusion_pkg/sensor_msg',self.listen,10,)
        self.client=self.create_client(LidarConfigSrv,"/sensor_fusion_pkg/configure_lidar")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = LidarConfigSrv.Request()

        self.publisher= self.create_publisher(ServoCtrlMsg,'/ctrl_pkg/servo_msg',1)
        timer_period = 0.1  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.angle=0.0
        self.throttle=1.0
      
        
       
    def send_request(self,):
        self.req.use_lidar=True
        self.req.min_angle= -179.0
        self.req.max_angle= 179.0
        self.req.num_values=60
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
        
        distance_matrix=np.concatenate((lidar_data[1:5],lidar_data[-5:]))

        least_distance=distance_matrix[np.argmin(distance_matrix)]
       
        
        if least_distance<1.0:
            self.angle=0.0
            self.throttle=0.0
        else:
            self.angle=0.0
            self.throttle=1.0
    

    
   


    def timer_callback(self):
        msg = ServoCtrlMsg()   
                                                    
        msg.angle= self.angle 
        msg.throttle= self.throttle
        self.publisher.publish(msg)
        print("message publisheds")
        print(msg.throttle)
        
       

           


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
