import numpy as np
import time
from simpleicp import PointCloud, SimpleICP


class EKF():

    def __init__(self) -> None:
        self.prev_point_cloud = np.array([])
        self.mu = np.zeros([3,1])
        self.Sigma = np.zeros([3,3])
        self.prev_time = 0
        self.dt = 0
        self.speed_scale = 0.5 ##NEED TO CHANGE BASED ON MEASUREMENTS
        self.angle_scale = np.pi/6 ##NEED TO CHANGE BASED ON MEASUREMENTS
        self.state_history = []
        self.cov_history = []
        self.L = 0.15 ##NEED TO CHANGE BASED ON MEASUREMENTS
        
    def bicycle_model(self,u1,dt):

        v = u1[0]*self.speed_scale
        
        dmu_dt = np.zeros([3,1])
        dmu_dt[0] = v*np.cos(self.mu[2])
        dmu_dt[1] = v*np.sin(self.mu[2])
        dmu_dt[2] = v*np.tan(u1[1] * self.angle_scale)/self.L

        dt_vect = np.zeros([3,1])
        dt_vect[0] = dt
        dt_vect[1] = dt
        dt_vect[2] = 0.1

        mu1 = self.mu + dmu_dt*dt_vect
        
        return mu1
    
    def EKF_step(self, u1, point_cloud, dt):

        #Noise variables
        Rt = np.ones([3,3])*0.1 + np.random.random([3,3])*0.1
        Qt = np.ones([3,3]) + np.random.random([3,3])*0.5

        #extract state and control variables for readability
        theta = self.mu[2]
        v = u1[0] * self.speed_scale

        #use bicycle model for predication step over one time step
        mu1_bar = self.bicycle_model(u1,dt)

        #calculate jacobian of bicycle model function
        Gt = np.eye(3,3)
        Gt[0,2] = -v*np.sin(theta)*dt
        Gt[1,2] = v*np.cos(theta)*dt

        #find prediction step covariance
        Sigma1_bar = np.matmul(Gt,np.matmul(self.Sigma,Gt.T)) + Rt

        #Sensor model is identity, Jacbian is identity
        Ht = np.eye(3,3)

        #find kalman gain
        Kt = np.matmul(Sigma1_bar,np.matmul(Ht.T,np.linalg.inv(np.matmul(Ht,np.matmul(Sigma1_bar,Ht.T))+Qt)))
     
        #determine the state estimate based on observations
        z1 = self.observation(point_cloud)

        print("mu1_bar = ", mu1_bar)
        print("z1 = ", z1)

        #Perform correction step on the mean and covariance of the state
        self.mu = mu1_bar + np.matmul(Kt,(z1 - mu1_bar))
        self.Sigma = np.matmul((np.eye(3,3) - np.matmul(Kt,Ht)),Sigma1_bar)
        print(z1-mu1_bar)
        print(Kt)
        print(np.matmul(Kt,(z1 - mu1_bar)))
        print("mu = ", self.mu)
        print("sigma = ", self.Sigma)
        print("dt = ", dt)

        self.state_history.append(self.mu.T)
        self.cov_history.append(self.Sigma)

        print(self.cov_history)
        print("")
        print(self.state_history)

        print(u1[1])
        
        np.savetxt("EKF_data.csv",np.array(self.state_history),delimiter=",")

    def observation(self,point_cloud):

        if(self.prev_point_cloud.size == 0):
            self.prev_point_cloud = point_cloud + np.random.random(point_cloud.shape)/100
        
        # Create point cloud objects
        pc_fix = PointCloud(self.prev_point_cloud, columns=["x", "y", "z"])
        pc_mov = PointCloud(point_cloud, columns=["x", "y", "z"])

        # Create simpleICP object, add point clouds, and run algorithm!
        icp = SimpleICP()
        icp.add_point_clouds(pc_fix, pc_mov)
        H, X_mov_transformed, rigid_body_transformation_params, distance_residuals = icp.run(max_overlap_distance=1, min_change = 20, max_iterations = 5)

        dstate = np.zeros([3,1])
        dstate[0] = rigid_body_transformation_params.tx.estimated_value
        dstate[1] = rigid_body_transformation_params.ty.estimated_value
        dstate[2] = np.deg2rad(rigid_body_transformation_params.alpha3.estimated_value)

        self.prev_point_cloud = np.copy(point_cloud) + np.random.random(point_cloud.shape)/100
        
        return self.mu + dstate


