import numpy as np
from driver_pkg.Filters import Filters
import math

class Driver():
    def __init__(self) -> None:
        self.filter=Filters()
        self.distance_matrix=np.array([])
        self.throttle=0.5
        self.angle=0.0

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, value):
        self.throttle = value

    def get_angle(self):
        return self.angle

    def set_angle(self, value):
        self.angle = value


    def get_controls(self,distance_matrix):
        self.distance_matrix=distance_matrix
        
        left_distances=self.distance_matrix[0:self.distance_matrix.size//2]
        right_distances=self.distance_matrix[self.distance_matrix.size//2+1 :]

        
        right_distances=right_distances[::-1]
        #print(right_distances)
        
        # logic start here 
        e=0 #self.scan_for_turn(left_distances,right_distances)
        if abs(e)>0:
            self.angle=float(e/90)
        else:
            self.angle= self.steer_between_walls(left_distances,right_distances)
        

    
    def scan_for_turn(self,left_distances,right_distances)-> int:
        

        left=self.filter.signal_smoothing_filter(left_distances[0:15])
        right=self.filter.signal_smoothing_filter(right_distances[0:15])
        
        #print(right,left)

        left_max_distance=left[np.argmax(left)]
        right_max_distance=right[np.argmax(right)]

        #print(left_max_distance,right_max_distance)
        if( right_max_distance>=left_max_distance and right_max_distance>=4.5):
                e=30+np.argmax(right)*6
                #print(-e)
                return -e
        elif( left_max_distance>right_max_distance and left_max_distance>=4.5):
                e=30+np.argmax(right)*6
                #print(-e)
                return e
      
        
        else:
            return 0
        
    def steer_between_walls(self,left_distances,right_distances):
        print('steer between walls')
        left = self.filter.signal_smoothing_filter(left_distances[12:18])
        right = self.filter.signal_smoothing_filter(right_distances[12:18])
        angle_matrix=np.array(range(12*6, 18*6,6))

        distance=right*np.sin(np.deg2rad(angle_matrix))

        print(distance)
        #print(angle_matrix)

        avg_left_distance = np.mean(left)
        #avg_right_distance = np.mean(right)
        avg_right_distance = np.mean(distance)

        #scaled_error = (avg_left_distance-avg_right_distance)/(avg_left_distance+avg_right_distance)
        scaled_error = 0.2-avg_right_distance
        steering_gain = 1/10
        steering_angle = steering_gain*scaled_error

        return steering_angle