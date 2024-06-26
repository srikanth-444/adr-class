import numpy as np
import cv2
#from skimage.feature import blob_doh
#import skimage.io
#from skimage.color import rgb2gray

class StopSignControl():
    def __init__(self) -> None:
        self.throttle=0.5
        self.angle=0.0
        self.go_count = 0
        self.stop_count = 0
        self.flag = 0
        self.stop_history = np.zeros([1,10])

    def get_throttle(self):
        return 0.45
        #return self.throttle

    def set_throttle(self, value):
        self.throttle = value

    def get_angle(self):
        return self.angle

    def set_angle(self, value):
        self.angle = value
        
    def get_flag(self):
        return self.flag

    def get_controls(self, image):
        
        sign_visible = self.stop_sign_visible(image)

        self.stop_history[:-1] = self.stop_history[1:]
        self.stop_history[-1] = sign_visible

        stop = np.sum(self.stop_history) > 3

        if(stop and self.stop_count < 75 and self.go_count > 75):

            self.throttle = 0.0
            self.flag = 1
            self.stop_count += 1

        else:

            if(self.stop_count > 0):
                self.stop_count = 0
                self.go_count = 0
                
            self.throttle = 0.5
            self.flag = 0
            self.go_count += 1


    def stop_sign_visible(self,image):

        red_layer = image[:, :, 0]
        green_layer = image[:, :, 1]
        blue_layer = image[:, :, 2]
        
        red_threshold = 150
        green_threshold = 150
        blue_threshold = 150
        active = (red_layer>red_threshold) * (green_layer < green_threshold) * (blue_layer < blue_threshold)
        red_layer[~active] = 0
        image[:,:,0] = red_layer
        image[:,:,1] = red_layer
        image[:,:,2] = red_layer
        image = 255-image
        for i in range(2):
            image = cv2.GaussianBlur(image,(15,15),cv2.BORDER_DEFAULT)

        red_layer = image[:, :, 0]
        
        active = red_layer < 100
        red_layer[active] = 0
        image[:,:,0] = red_layer
        image[:,:,1] = red_layer
        image[:,:,2] = red_layer

        # print(np.mean(red_layer))
        
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        
        # # Change thresholds
        # params.minThreshold = 10
        # params.maxThreshold = 200
        
        
        # Filter by Area.
        # params.filterByArea = True
        # params.minArea = 1
        # params.maxArea = 10000
        
        # # Filter by Circularity
        # params.filterByCircularity = True
        # params.minCircularity = 0.8
        
        # # Filter by Convexity
        # params.filterByConvexity = True
        # params.minConvexity = 0.8
        
        # # Filter by Inertia
        # params.filterByInertia = True
        # params.minInertiaRatio = 0.01
        
        detector = cv2.SimpleBlobDetector_create(params)
        
        # Detect blobs.
        keypoints = detector.detect(image)
         
        #print(len(keypoints))
        if(len(keypoints) > 0):
             return 1
        else:
             return 0
        
        
