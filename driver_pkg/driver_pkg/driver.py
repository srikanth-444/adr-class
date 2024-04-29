import numpy as np
from driver_pkg.Filters import Filters
from driver_pkg.Visuals import Visuals


class Driver():
    def __init__(self) -> None:
        self.filter=Filters()
        self.distance_matrix=np.array([])
        self.throttle=0.5
        self.angle=0.0
        self.flag=0
        self.viz=Visuals()
        

    def get_flag(self):
        return self.flag

    def set_flag(self, value):
        self.flag = value


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
        e=self.scan_for_turn(left_distances,right_distances)
        if abs(e)>0:
            self.angle=e
            self.flag=1
        else:
            self.angle= self.steer_between_walls(left_distances,right_distances)
            self.flag=0
        

    
    def scan_for_turn(self,left_distances,right_distances)-> int:
        
        
        #left=left_distances[30:90]
        right=self.filter.signal_smoothing_filter(right_distances[60:90])
        angle_matrix=np.array(range(55,85,1))
        #front_right=self.filter.signal_smoothing_filter(right_distances[0:5])
        #front_left=self.filter.signal_smoothing_filter(left_distances[0:5])

        #self.viz.set_distance(right)
        #self.viz.get_visuals()
        
        #print(right,left)

        # for i in range(3):
        #       right[i] = min([5,right[i]])
        #       left[i] = min([5,left[i]])

        #left_max_distance=left[np.argmax(left)]
        #right_max_distance=right[np.argmax(right)]
        #front_right_max_distance=max(front_right)
        #front_left_max_distance=max(front_left)

        x= right *np.sin(np.deg2rad(angle_matrix))
        #print(left_max_distance,right_max_distance,front_right_max_distance)
        # if( right_max_distance>=left_max_distance and right_max_distance>=4.5):
        #         e=np.argmax(right)*6
        #         #print(-e)
        #         return -e
        # # elif( front_right_max_distance>=front_left_max_distance and front_right_max_distance>=4):
        # #           e=np.argmax(front_right)*6
        # #          #print(-e)
        # #           return -e
        # elif( left_max_distance>right_max_distance and left_max_distance>=4.5):
        #          e=30+np.argmax(left)*6
        #          #print(-e)
        #          return e
        r_avg=np.mean(x)
        print(r_avg)
        if r_avg>3.8:
            return -1.0
        else:
            return 0.0
        
    
        
    def steer_between_walls(self,left_distances,right_distances):
        #print('steer between walls')
        left = left_distances[60:120]
        right =right_distances[60:120]
        angle_matrix=np.array(range(60, 120,1))

        right_distance= right *np.sin(np.deg2rad(angle_matrix))
        left_distance = left *np.sin(np.deg2rad(angle_matrix))
        #print(distance)
        #print(angle_matrix)

        avg_left_distance = np.min([1,np.mean(left_distance)])
        avg_right_distance = np.min([1,np.mean(right_distance)])
        #avg_right_distance = np.mean(distance)
        #avg_right_distance = np.min(distance)
        #print(avg_right_distance)
        #print(avg_left_distance)

        scaled_error = (avg_left_distance-avg_right_distance)/(avg_left_distance+avg_right_distance)
        #scaled_error = 0.3-avg_right_distance
        steering_gain = 0.2
        steering_angle = steering_gain*scaled_error
        

        return steering_angle