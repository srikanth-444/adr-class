import rclpy
from rclpy.node import Node

import time


class Distance(Node):
    def __init__(self):
        super().__init__('subcriber')
        print("hello")

def main(args=None):
    rclpy.init(args=args)

    distance=Distance()

    try:
        rclpy.spin(distance)
    except SystemExit:
        distance.destroy_node()

