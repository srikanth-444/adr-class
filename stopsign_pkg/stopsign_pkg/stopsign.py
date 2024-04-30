import numpy as np
from skimage.feature import blob_doh
import skimage.io
from skimage.color import rgb2gray

class StopSign():
    def __init__(self) -> None:
        self.filter=Filters()
        self.throttle=0.0
        self.angle=0.0
        self.previosuly_stopped = False

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, value):
        self.throttle = value

    def get_angle(self):
        return self.angle

    def set_angle(self, value):
        self.angle = value

    def get_controls(self, image):
        
        stop = self.stop_sign_visible(image)

        if(stop):

            if(self.previously_stopped):
                self.throttle = 0.5
            else:
                self.throttle = 0
                self.previously_stopped = True
        else:
            
            self.throttle = 0.5
            if(self.previously_stopped):
                self.previously_stopped = False


    def stop_sign_visible(self,image):

        red_layer = image[:, :, 0]
        red_threshold = 240
        active = red_layer>red_threshold
        red_layer[~active] = 0
        image[:,:,1] = red_layer
        image[:,:,2] = red_layer
        gray_image = rgb2gray(image)
        blobs1 = blob_doh(gray_image, max_sigma=100, threshold=0.01)
        stop_size = 100
        biggest_blobs = blobs1[:,2]>stop_size
        
        if(len(biggest_blobs > 0)):
            return True
        
        return False
        
        
