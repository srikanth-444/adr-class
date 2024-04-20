import numpy as np

class Driver():
    def __init__(self) -> None:
        self.distance_matrix=np.array([])
        self.throttle=0.0
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
        
        left_distances=self.distance_matrix[1:self.distance_matrix.size//2-1]
        right_distances=self.distance_matrix[self.distance_matrix.size//2+1 :]
        
        # logic start here 
        e=self.scan_for_turn(left_distances,right_distances)
        if abs(e)>0:
            self.angle=float(e/90)
        else:
            self.angle=0.0
        

    
    def scan_for_turn(self,left_distances,right_distances)-> int:
        
        left=left_distances
        right=right_distances
        
        print(len(left))

        left_max_distance=left[np.argmax(left)]
        right_max_distance=right[np.argmax(right)]


        if (left_max_distance>right_max_distance and left_max_distance>=0.5):
                e=30+np.argmax(left)
                return e
        elif(right_max_distance>left_max_distance and right_max_distance>=0.5):
                e=30+np.argmax(right)
                return -e
        else:
            return 0