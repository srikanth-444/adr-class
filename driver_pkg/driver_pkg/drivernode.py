import rclpy
from rclpy.node import Node
import numpy as np
from driver_pkg.driver import Driver
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
    
from deepracer_interfaces_pkg.msg import EvoSensorMsg
from deepracer_interfaces_pkg.srv import LidarConfigSrv
from deepracer_interfaces_pkg.msg import ServoCtrlMsg
    
    
class Drive(Node):

    def __init__(self):
        super().__init__('Drive')
        self.lidar_message_sub_cb_grp = ReentrantCallbackGroup()
        #client for configuring lidar
        self.lidar_client=self.create_client(LidarConfigSrv,"/sensor_fusion_pkg/configure_lidar")
        while not self.lidar_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = LidarConfigSrv.Request()


        #lidar data subscriber
        self.lidar_subcriber= self.create_subscription(EvoSensorMsg, '/sensor_fusion_pkg/sensor_msg',self.lidar_listen,10,callback_group=self.lidar_message_sub_cb_grp)
        
        # steering publisher
        self.steering_publisher= self.create_publisher(ServoCtrlMsg,'/ctrl_pkg/servo_msg',1)

        timer_period = 0.1

        self.timer = self.create_timer(timer_period, self.drive_timer_callback)

        #initial values of steering and throttle
        self.angle=0.0
        self.throttle=0.0
        self.driver=Driver()
        self.distance_matrix=np.array([])

    def set_lidar_configuration(self,):
        self.req.use_lidar=False
        #setting up the area of scan       
        self.req.min_angle= -179.0
        self.req.max_angle= 179.0
        # sets the number of points in array 
        self.req.num_values=61 
        # doesn't scan the objects less than this distance(m)
        self.req.min_distance=0.10
        # doesn't scan the objects greater than this distance(m)
        self.req.max_distance=12.0
        # clips the distance greater than self.clipping_distance to self.clipping_distance
        self.req.clipping_distance=12.0
        self.req.num_sectors=60
        self.req.preprocess_type=0
        self.future = self.lidar_client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()                      

    def lidar_listen(self, msg):
        self.distance_matrix=np.array(msg.lidar_data)
        
        self.driver.get_controls(self.distance_matrix)
        self.angle=self.driver.get_angle()
        self.throttle=self.driver.get_throttle()
        self.flag=self.driver.get_flag()
    

    def drive_timer_callback(self):
        msg = ServoCtrlMsg()   
                                                    
        msg.angle= self.angle 
        msg.throttle= self.throttle
        self.steering_publisher.publish(msg)
        self.get_logger().info("message published steering : %f throttle: %f flag: %f"%(msg.angle,msg.throttle,float(self.flag)))
     
        
       

           


def main(args=None):
    rclpy.init(args=args)

    drive = Drive()
    try:
        try:
            res=drive.set_lidar_configuration()
            if (res.error==1):
                raise Exception
            

        except:
            drive.get_logger().error("lidar config wrong you idiot")
            rclpy.shutdown()
    

        drive.get_logger().info('lidar has been configured')
        executor = MultiThreadedExecutor()
        rclpy.spin(drive,executor)
    except KeyboardInterrupt:
        msg = ServoCtrlMsg()   
        drive.angle=0.0
        drive.throttle=0.0                                      
        msg.angle= drive.angle 
        msg.throttle= drive.throttle
        drive.steering_publisher.publish(msg)
        drive.get_logger().info("message published steering : %f throttle: %f" %(msg.angle,msg.throttle))

        drive.destroy_node()
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()
