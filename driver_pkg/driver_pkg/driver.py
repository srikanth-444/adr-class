import numpy as np
from driver_pkg.Filters import Filters
from driver_pkg.Visuals import Visuals
from time import time



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
        "y":narrow_webVisuals.y_data
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
    def __init__(self) -> None:
        self.filter=Filters()
        self.distance_matrix=np.array([])
        self.throttle=0.5
        self.angle=0.0
        self.flag=0
        self.viz=Visuals()
        self.in_wall=1.5
        self.start_time=time()
        self.e_matrix=[]
        self.time_m=[]
        self.saturation=0.15
        self.turn_counter = 0
        self.start_time=time()
        self.previous_error=0
        
        

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
        
        if(self.flag == 1 and self.turn_counter < 15):
            self.flag = 1
            self.angle = -1.0
            self.turn_counter += 1
        else:

            if(self.turn_counter >= 15):
                self.turn_counter = 0

            left_distances=self.distance_matrix[0:self.distance_matrix.size//2]
            right_distances=self.distance_matrix[self.distance_matrix.size//2+1 :]

            
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
            # elif(abs(e)>0):
            #      self.angle=float(e/90)
            #      self.flag=2
            else:
                time_step=self.start_time-time()
                v_e=(s_e-self.previous_error)/time_step
                self.angle= float(s_e+v_e*0.1)
                self.flag=0
                self.start_time=time()
                self.previous_error=s_e
            
        

    
    def scan_for_turn(self,left_distances,right_distances):
        
        
        #left=left_distances[30:90]
        right=self.filter.signal_smoothing_filter(right_distances[45:90])
        angle_matrix=np.array(range(45,90,1))
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
        y= right *np.cos(np.deg2rad(angle_matrix))

        right_steer_webVsiuals.x_data=x.tolist()
        right_steer_webVsiuals.y_data=y.tolist()
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
        if r_avg>7.5:
            
            return -1.0
        else:
            return 0.0
        
    def steering_narrow(self,left_distances,right_distances):
        front_right=np.clip(right_distances[15:30],0.1,1)
        front_left=np.clip(left_distances[15:30],0.1,1)
        angle_matrix=np.array(range(15,30,1))
        left_x=front_left* np.sin(np.deg2rad(angle_matrix))
        right_x=front_right* np.sin(np.deg2rad(angle_matrix))
        left_y=front_left* np.cos(np.deg2rad(angle_matrix))
        right_y=front_right* np.cos(np.deg2rad(angle_matrix))
    
        narrow_webVisuals.x_data=np.concatenate((np.negative(left_x[::-1]),right_x)).tolist()
        narrow_webVisuals.y_data=np.concatenate((left_y[::-1],right_y)).tolist()
        front_right_max_distance=np.mean(front_right)
        front_left_max_distance=np.mean(front_left)
        print(front_right_max_distance,front_left_max_distance)
        if( front_right_max_distance>front_left_max_distance and front_right_max_distance>=0.5):
                e=15+np.argmax(front_right)
                print(e)
                return -e
        elif( front_left_max_distance>front_right_max_distance and front_left_max_distance>=0.5):
                e=15+np.argmax(front_left)
                return e
        else:
            return 0

        
    def steer_between_walls(self,left_distances,right_distances):

        
        
        #print('steer between walls')
        left = left_distances[30:90]
        right =right_distances[30:90]
        angle_matrix=np.array(range(30, 90,1))

        right_x= np.clip(right *np.sin(np.deg2rad(angle_matrix)),0.1,self.in_wall)
        left_x = np.clip(left *np.sin(np.deg2rad(angle_matrix)),0.1,self.in_wall)
        left_y=left* np.cos(np.deg2rad(angle_matrix))
        right_y=right* np.cos(np.deg2rad(angle_matrix))

        steer_btween_walls.x_data=np.concatenate((np.negative(left_x[::-1]),right_x)).tolist()
        steer_btween_walls.y_data=np.concatenate((left_y[::-1],right_y)).tolist()
        #print(distance)
        #print(angle_matrix)
        
        #avg_left_distance = np.min([self.in_wall,np.mean(left_distance)])
        #avg_right_distance = np.min([self.in_wall,np.mean(right_distance)])
    
        avg_right_distance = np.mean(right_x[30:120])
        avg_left_distance = np.min(left_x[30:120])
        #print(avg_right_distance)
        #print(avg_left_distance)

        scaled_error = (avg_left_distance-avg_right_distance)/(avg_left_distance+avg_right_distance)
        
        
        #scaled_error = 0.3-avg_right_distance

        if scaled_error>self.saturation:
            scaled_error=self.saturation
        elif scaled_error<-self.saturation:
            scaled_error=-self.saturation
       
        return scaled_error
    

