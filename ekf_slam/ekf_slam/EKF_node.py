import rclpy
from rclpy.node import Node
import numpy as np
from ekf_slam.EKF import EKF
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import threading
from time import time
    
from deepracer_interfaces_pkg.msg import EvoSensorMsg
from deepracer_interfaces_pkg.srv import LidarConfigSrv
from deepracer_interfaces_pkg.msg import ServoCtrlMsg
    
    
class EKF_node(Node):

    def __init__(self):
        super().__init__('EKF_node')

        self.lidar_message_sub_cb_grp = ReentrantCallbackGroup()
        self.control_message_sub_cb_grp = ReentrantCallbackGroup()

        #lidar data subscriber
        self.lidar_subcriber= self.create_subscription(EvoSensorMsg, '/sensor_fusion_pkg/sensor_msg',self.lidar_listen,10,callback_group=self.lidar_message_sub_cb_grp)
        
        #controls subscriber
        self.control_subcriber= self.create_subscription(ServoCtrlMsg, '/ctrl_pkg/servo_msg',self.control_listen,10,callback_group=self.control_message_sub_cb_grp)
        
        self.EKF = EKF()
        
        self.angle_matrix = range(-179,180)
        self.point_cloud = np.array([])

        self.dt = 0.1

    def lidar_listen(self, msg):

        distance_matrix=np.array(msg.lidar_data)
        xvals = distance_matrix *np.sin(np.deg2rad(self.angle_matrix))
        yvals = distance_matrix *np.cos(np.deg2rad(self.angle_matrix))
        
        self.point_cloud = []
        for x, y in zip(xvals,yvals):
            self.point_cloud.append(np.array([x,y,0]))
        self.point_cloud = np.array(self.point_cloud)

    def control_listen(self,msg):

        start_time = time()
        u = np.array([msg.throttle,msg.angle])
        self.EKF.EKF_step(u,self.point_cloud,self.dt)
        self.dt = time()-start_time

    

def main(args=None):
    rclpy.init(args=args)

    ekf_node = EKF_node()
    try:
        executor = MultiThreadedExecutor()
        rclpy.spin(ekf_node,executor)
    except KeyboardInterrupt:

        ekf_node.destroy_node()
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()
