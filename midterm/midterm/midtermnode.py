import rclpy
from rclpy.node import Node
    
from deepracer_interfaces_pkg.msg import EvoSensorMsg
    
    
class Distance_Calculator(Node):

    def __init__(self):
        super().__init__('distance_calculator')
        self.subcriber= self.create_subscription(EvoSensorMsg, 'topic',self.listen,10,)
        self.data_subscriber=[]
       
                            

    def listen(self, msg):
        
        lidar_data = msg.lidar_data 
        
        self.data_subscriber.append(lidar_data)
        self.get_logger().info(lidar_data)
   

       

           


def main(args=None):
    rclpy.init(args=args)

    distance_calculator = Distance_Calculator()

    rclpy.spin(distance_calculator)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    distance_calculator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
