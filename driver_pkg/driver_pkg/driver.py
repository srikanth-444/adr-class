import numpy as np
from driver_pkg.Filters import Filters
from driver_pkg.Visuals import Visuals
from time import time
from scipy.stats import linregress
import math




from flask import Blueprint,request, jsonify



class Webvisual():
    def __init__(self) -> None:
        
        self.x_data=[]
        self.y_data=[]

stop=0

Lidar_BLUEPRINT = Blueprint("Lidar", __name__)
narrow_webVisuals=Webvisual()
right_steer_webVsiuals=Webvisual()
steer_btween_walls=Webvisual()
w_error = Webvisual()
points = Webvisual()

@Lidar_BLUEPRINT.route('/rightTurnLidar', methods=["GET", "POST"])
def rightlidar():
    data ={
        "x":right_steer_webVsiuals.x_data,
        "y":right_steer_webVsiuals.y_data
    }
    return data
@Lidar_BLUEPRINT.route('/narrowLidar', methods=["GET", "POST"])
def narrowlidar():
    data ={
        "x":narrow_webVisuals.x_data,
        "y":narrow_webVisuals.y_data,
        "x1":points.x_data,
        "y1":points.y_data
    }
    return data
@Lidar_BLUEPRINT.route('/betweenWallsLidar', methods=["GET", "POST"])
def betweenlidar():
    data ={
        "x":steer_btween_walls.x_data,
        "y":steer_btween_walls.y_data
        
    }
    return data
@Lidar_BLUEPRINT.route('/error', methods=["GET", "POST"])
def W_error():
    data ={
        "x":w_error.x_data[-10:],
        "y":w_error.y_data[-10:]
    }
    return data

@Lidar_BLUEPRINT.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json.get('data')  # Get the 'data' field from the JSON payload
    # Process the received data
    stop=data
    print("Received data from JS:", stop)
    # Return a response
    return jsonify({'message': 'Data received successfully'})



class Driver():
    def __init__(self,mode) -> None:

        self.mode=mode
        self.filter=Filters()
        self.distance_matrix=np.array([])
        if self.mode==1:
            self.throttle=0.5
        if self.mode==0:
            self.throttle=-0.5    
        self.angle=0.0
        self.flag=0
        self.viz=Visuals()
        self.in_wall=3




        self.start_time=time()
        self.e_matrix=[]
        self.time_m=[]
        self.saturation=60/90
        self.turn_counter = 0
        self.start_time=time()
        self.previous_error=0
        self.previous_o_error=0
        self.x_gain= 2.2
        self.o_gain=0.08
        
        

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
        
        if(self.flag == 1 and self.turn_counter< 15 ):
            self.flag = 1
            self.angle = -1.0
            self.turn_counter += 1
        else:

            if(self.turn_counter >= 15):
                self.turn_counter = 0


            if self.mode==1:
                left_distances=self.distance_matrix[0:self.distance_matrix.size//2]
                right_distances=self.distance_matrix[self.distance_matrix.size//2+1 :]
            if self.mode==0:
                left_distances=self.distance_matrix[0:self.distance_matrix.size//2]
                right_distances=self.distance_matrix[self.distance_matrix.size//2+1 :]
                tmp=right_distances
                right_distances=left_distances
                left_distances=tmp


            right_distances=right_distances[::-1]
            #print(right_distances)
            
            # logic start here 
            a=self.scan_for_turn(left_distances,right_distances)
            e=self.steering_narrow(left_distances,right_distances)
            s_e=self.steer_between_walls(left_distances,right_distances)


            self.e_matrix.append(s_e)
            self.time_m.append(time())

            w_error.y_data=self.e_matrix
            w_error.x_data=self.time_m

            if abs(a)>0:
                self.angle=a
                self.flag=1
            else:
                time_step=self.start_time-time()
                #print(time_step)
                v_e=(s_e-self.previous_error)/time_step
                v_o_e=(e-self.previous_o_error)/time_step
                #print(s_e,e)
                scaled_error=float(s_e*self.x_gain+e*self.o_gain)#v_o_e*0.1)
               
                self.angle= scaled_error
                self.flag=0
                self.start_time=time()
                self.previous_error=s_e
                self.previous_o_error=e
            
        

    
    def scan_for_turn(self,left_distances,right_distances):
        
        
        
        right=right_distances[45:90]
        angle_matrix=np.array(range(45,90,1))

        x= right *np.sin(np.deg2rad(angle_matrix))
        y= right *np.cos(np.deg2rad(angle_matrix))

        right_steer_webVsiuals.x_data=x.tolist()
        right_steer_webVsiuals.y_data=y.tolist()
     
        r_avg=np.mean(x)
        
        #print(r_avg)
        if r_avg>7.5:
            
            return -1.0
        else:
            return 0.0
        
    def steering_narrow(self,left_distances,right_distances):
        front_right=np.clip(right_distances[15:165],0.1,12)
        front_left=np.clip(left_distances[15:165],0.1,12)

        

        angle_matrix=np.array(range(15,165,1))
        left_x=front_left* np.sin(np.deg2rad(angle_matrix))
        right_x=front_right* np.sin(np.deg2rad(angle_matrix))
        left_y=front_left* np.cos(np.deg2rad(angle_matrix))
        right_y=front_right* np.cos(np.deg2rad(angle_matrix))

        #print(left_x,right_x)
        r_indices=np.argwhere(right_x<1.5).flatten()
        l_indices=np.argwhere(left_x<1.5).flatten()
        r_x=[]
        r_y=[]
        l_x=[]
        l_y=[]

        for i in r_indices:
            r_x.append(right_x[i])
            r_y.append(right_y[i])

        for i in l_indices:
            l_x.append(left_x[i])
            l_y.append(left_y[i])
        
        if not r_x:
            
            r_regression_line = np.linspace(-1,1,num=10)   
            r_x=np.ones_like(r_regression_line)
            r_slope=np.inf
        else:
            r_slope, r_intercept, r_value, p_value, std_err = linregress(r_x, r_y)
            r_regression_line = r_slope * np.array(r_x) + r_intercept    
        
        if not l_x:
            l_regression_line = np.linspace(-1,1,num=10)   
            l_x=np.ones_like(l_regression_line)
            l_slope=np.inf
        else:
            l_slope, l_intercept, r_value, p_value, std_err = linregress(l_x, l_y)
            l_regression_line = l_slope * np.array(l_x) + l_intercept
        narrow_webVisuals.x_data=np.concatenate((np.negative(l_x[::-1]),r_x)).tolist()
        narrow_webVisuals.y_data=np.concatenate((l_regression_line[::-1],r_regression_line)).tolist()

        points.x_data=np.concatenate((np.negative(l_x[::-1]),r_x)).tolist()
        points.y_data=np.concatenate((l_y[::-1],r_y)).tolist()
       

        #print(r_slope,l_slope)

        r_angle_with_y=math.degrees(np.arctan(-1/r_slope))
        l_angle_with_y=math.degrees(np.arctan(-1/l_slope))

        #print(r_angle_with_y,l_angle_with_y)

        e = (r_angle_with_y - l_angle_with_y)/2

        return math.radians(e)

        
    def steer_between_walls(self,left_distances,right_distances):

        
        
        #print('steer between walls')
        left = np.clip(left_distances,0.1,5)
        right =np.clip(right_distances,0.1,5)

        


        angle_matrix=np.array(range(0, 179,1))

        right_x= right *np.sin(np.deg2rad(angle_matrix))
        left_x = left *np.sin(np.deg2rad(angle_matrix))
        left_y=left* np.cos(np.deg2rad(angle_matrix))
        right_y=right* np.cos(np.deg2rad(angle_matrix))

        
        steer_btween_walls.x_data=np.concatenate((np.negative(left_x[::-1]),right_x)).tolist()
        steer_btween_walls.y_data=np.concatenate((left_y[::-1],right_y)).tolist()
        #print(distance)
        #print(angle_matrix)
       
        r_indices=np.argwhere(right_x<1.5).flatten()
        l_indices=np.argwhere(left_x<1.5).flatten()
        r_x=[]
        r_y=[]
        l_x=[]
        l_y=[]

        for i in r_indices:
            r_x.append(right_x[i])
            r_y.append(right_y[i])

        for i in l_indices:
            l_x.append(left_x[i])
            l_y.append(left_y[i])

        if not r_x:
            avg_right_distance=1.5
        else:
            
            avg_right_distance = np.mean(r_x)

        if not l_x:
            avg_left_distance=1.5
        else:
            avg_left_distance = np.mean(l_x)-0.05
        #print(avg_right_distance)
        #print(avg_left_distance)

        scaled_error = (avg_left_distance-avg_right_distance)/(avg_left_distance+avg_right_distance)
        
        
    
       
        return scaled_error
    

