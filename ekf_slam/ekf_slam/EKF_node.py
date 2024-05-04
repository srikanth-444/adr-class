import rclpy
from rclpy.node import Node
import numpy as np
from ekf_slam.EKF import EKF
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import threading
import time
    
from deepracer_interfaces_pkg.msg import EvoSensorMsg
from deepracer_interfaces_pkg.srv import LidarConfigSrv
from deepracer_interfaces_pkg.msg import ServoCtrlMsg
    
    
class EKF_node(Node):

    def __init__(self):
        super().__init__('EKF_node')

        self.lidar_message_sub_cb_grp = ReentrantCallbackGroup()
        self.control_message_sub_cb_grp = ReentrantCallbackGroup()

        #client for configuring lidar
        self.lidar_client=self.create_client(LidarConfigSrv,"/sensor_fusion_pkg/configure_lidar")
        while not self.lidar_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = LidarConfigSrv.Request()


        #lidar data subscriber
        self.lidar_subcriber= self.create_subscription(EvoSensorMsg, '/sensor_fusion_pkg/sensor_msg',self.lidar_listen,10,callback_group=self.lidar_message_sub_cb_grp)
        
        #controls subscriber
        self.control_subcriber= self.create_subscription(ServoCtrlMsg, '/ctrl_pkg/servo_msg',self.control_listen,10,callback_group=self.control_message_sub_cb_grp)
        
        self.EKF = EKF()
        
        self.angle_matrix = range(-179,180)
        self.point_cloud = np.array([])

        self.dt = 0.1


    def set_lidar_configuration(self,):
        self.req.use_lidar=False
        #setting up the area of scan       
        self.req.min_angle= -179.0
        self.req.max_angle= 179.0
        # sets the number of points in array 
        self.req.num_values=359 
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

        distance_matrix=np.array(msg.lidar_data)
        xvals = distance_matrix *np.sin(np.deg2rad(self.angle_matrix))
        yvals = distance_matrix *np.cos(np.deg2rad(self.angle_matrix))
        
        self.point_cloud = []
        for x, y in zip(xvals,yvals):
            self.point_cloud.append(np.array([x,y,0]))
        self.point_cloud = np.array(self.point_cloud)

    def control_listen(self,msg):

        start_time = time.time()
        u = np.array([msg.throttle,msg.angle])
        self.EKF.EKF_step(u,self.point_cloud,self.dt)
        self.dt = time.time()-start_time

    

def main(args=None):
    rclpy.init(args=args)

    ekf_node = EKF_node()
    try:
        try:
            res=ekf_node.set_lidar_configuration()
            if (res.error==1):
                raise Exception
            

        except:
            ekf_node.get_logger().error("lidar config wrong you idiot")
            rclpy.shutdown()
    

        ekf_node.get_logger().info('lidar has been configured')
        executor = MultiThreadedExecutor()
        rclpy.spin(ekf_node,executor)
    except KeyboardInterrupt:
        # msg = ServoCtrlMsg()   
        # drive.angle=0.0
        # drive.throttle=0.0                                      
        # msg.angle= drive.angle 
        # msg.throttle= drive.throttle
        # drive.steering_publisher.publish(msg)
        # drive.get_logger().info("message published steering : %f throttle: %f" %(msg.angle,msg.throttle))

        ekf_node.destroy_node()
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()
