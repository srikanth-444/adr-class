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
        self.speed_scale = 2 ##NEED TO CHANGE BASED ON MEASUREMENTS
        self.state_history = []
        self.cov_history = []
        
    def bicycle_model(self,u1,dt):

        L = 0.2 ##NEED TO CHANGE BASED ON MEASUREMENTS
        v = u1[0]*self.speed_scale
        
        dmu_dt = np.zeros([3,1])
        dmu_dt[0] = v*np.cos(self.mu[2])
        dmu_dt[1] = v*np.sin(self.mu[2])
        dmu_dt[2] = v*np.tan(u1[1])/L

        mu1 = self.mu + dmu_dt*dt
        
        return mu1
    
    def EKF_step(self, u1, point_cloud, dt):

        #Noise variables
        Rt = np.zeros([3,3])
        Qt = np.zeros([3,3])

        #extract state and control variables for readability
        theta = self.mu[2]
        v = u1[0] * self.speed_scale

        #use bicycle model for predication step over one time step
        mu1_bar = self.bicycle_model(u1,dt)

        #calculate jacobian of bicycle model function
        Gt = np.eye(3)
        Gt[0,2] = -v*np.sin(theta)*dt
        Gt[1,2] = v*np.cos(theta)*dt
        
        Sigma1_bar = Gt*self.Sigma*Gt.T + Rt

        #Sensor model is identity, Jacbian is identity
        Ht = np.eye(3)

        #find kalman gain
        Kt = Sigma1_bar*Ht.T*np.linalg.inv(Ht*Sigma1_bar*Ht.T+Qt)
        
        #determine the state estimate based on observations
        z1 = self.observation(point_cloud)

        #Perform correction step on the mean and covariance of the state
        self.mu = mu1_bar + Kt*(z1 - mu1_bar)
        self.Sigma = (np.eye([3,3]) - Kt*Ht)*Sigma1_bar

        self.state_history.append(self.mu)
        self.cov_history.append(self.Sigma)

    def observation(self,mu,point_cloud):

        # Create point cloud objects
        pc_fix = PointCloud(self.prev_point_cloud, columns=["x", "y", "z"])
        pc_mov = PointCloud(point_cloud, columns=["x", "y", "z"])

        # Create simpleICP object, add point clouds, and run algorithm!
        icp = SimpleICP()
        icp.add_point_clouds(pc_fix, pc_mov)
        H, X_mov_transformed, rigid_body_transformation_params, distance_residuals = icp.run(max_overlap_distance=1)

        dstate = np.zeros([3,1])
        dstate[2] = rigid_body_transformation_params[2]
        dstate[0] = rigid_body_transformation_params[3]
        dstate[1] = rigid_body_transformation_params[4]

        self.prev_point_cloud = point_cloud
        
        return mu + dstate


