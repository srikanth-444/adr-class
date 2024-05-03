import numpy as np
import cv2
#from skimage.feature import blob_doh
#import skimage.io
#from skimage.color import rgb2gray

class StopSignControl():
    def __init__(self) -> None:
        self.throttle=0.0
        self.angle=0.0
        self.previously_stopped = False
        self.flag = 0

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, value):
        self.throttle = value

    def get_angle(self):
        return self.angle

    def set_angle(self, value):
        self.angle = value
        
    def get_flag(self):
        return self.flag

    def get_controls(self, image):
        
        stop = self.stop_sign_visible(image)

        if(stop):

            if(self.previously_stopped):
                self.throttle = 0.5
                self.flag = 2
            else:
                self.throttle = 0.0
                self.previously_stopped = True
                self.flag = 1
        else:
            
            self.throttle = 0.5
            self.flag = 0
            if(self.previously_stopped):
                self.previously_stopped = False

        self.throttle = 0.0


    def stop_sign_visible(self,image):

        red_layer = image[:, :, 0]
        red_threshold = 100
        active = red_layer>red_threshold
        red_layer[~active] = 0
        image[:,:,1] = red_layer
        image[:,:,2] = red_layer
        
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        
        # # Change thresholds
        # params.minThreshold = 10
        # params.maxThreshold = 200
        
        
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 10
        params.maxArea = 3000
        
        # # Filter by Circularity
        # params.filterByCircularity = True
        # params.minCircularity = 0.1
        
        # Filter by Convexity
        # params.filterByConvexity = True
        # params.minConvexity = 0.8
        
        # # Filter by Inertia
        # params.filterByInertia = True
        # params.minInertiaRatio = 0.01
        
        # Create a detector with the parameters
        # OLD: detector = cv2.SimpleBlobDetector(params)
        detector = cv2.SimpleBlobDetector_create(params)
        
        # Detect blobs.
        keypoints = detector.detect(image)
        # gray_image = rgb2gray(image)
        # blobs1 = blob_doh(gray_image, max_sigma=100, threshold=0.01)
        # stop_size = 100
        # biggest_blobs = blobs1[:,2]>stop_size
        print(len(keypoints))
        if(len(keypoints) > 0):
             print(keypoints)
             return True
        
        return False
        
        
