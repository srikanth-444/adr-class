import rclpy
from rclpy.node import Node
import numpy as np
from stopsign_pkg.stopsigncontrol import StopSignControl
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from sensor_msgs.msg import Image
from custom_msg.msg import Throttle

from cv_bridge import CvBridge, CvBridgeError

    
    
class StopSign(Node):

    def __init__(self):
        super().__init__('StopSign')

        ###?????
        self.camera_message_sub_cb_grp = ReentrantCallbackGroup()

        #camera image subscriber
        self.image_subcriber= self.create_subscription(Image, '/camera_pkg/display_mjpeg',self.camera_listen,10,callback_group=self.camera_message_sub_cb_grp)
        
        # steering publisher
        self.steering_publisher= self.create_publisher(Throttle,'/stop_sign/throttle',1)

        timer_period = 0.1/3

        self.timer = self.create_timer(timer_period, self.drive_timer_callback)

        #initial values of steering and throttle
        self.angle=0.0
        self.throttle=0.0
        self.stopsign = StopSignControl()
        self.bridge = CvBridge()
        self.flag=0.0


    def camera_listen(self, msg):

        try:
            image = self.bridge.imgmsg_to_cv2(msg,"rgb8")
        except CvBridgeError as e:
            print(e)

        self.stopsign.get_controls(image)
        self.throttle=self.stopsign.get_throttle()
        self.flag=self.stopsign.get_flag()
    

    def drive_timer_callback(self):
        msg = Throttle()   
        msg.throttle= self.throttle
        self.steering_publisher.publish(msg)
        self.get_logger().info("message published throttle: %f flag: %f"%(msg.throttle,float(self.flag)))
     
        
       

           


def main(args=None):
    rclpy.init(args=args)

    stopsign = StopSign()
    try:
        stopsign.get_logger().info('ready to execute')
        executor = MultiThreadedExecutor()
        rclpy.spin(stopsign,executor)
    except KeyboardInterrupt:
        msg = Throttle()   
        stopsign.angle=0.0
        stopsign.throttle=0.0                                      
        
        msg.throttle= stopsign.throttle
        stopsign.steering_publisher.publish(msg)
        stopsign.get_logger().info("message published throttle: %f" %(msg.throttle))

        stopsign.destroy_node()
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()
