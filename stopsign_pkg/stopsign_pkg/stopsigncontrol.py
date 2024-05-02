import numpy as np
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

        # red_layer = image[:, :, 0]
        # red_threshold = 240
        # active = red_layer>red_threshold
        # red_layer[~active] = 0
        # image[:,:,1] = red_layer
        # image[:,:,2] = red_layer
        # gray_image = rgb2gray(image)
        # blobs1 = blob_doh(gray_image, max_sigma=100, threshold=0.01)
        # stop_size = 100
        # biggest_blobs = blobs1[:,2]>stop_size
        
        # if(len(biggest_blobs > 0)):
        #     return True
        
        return False
        
        
