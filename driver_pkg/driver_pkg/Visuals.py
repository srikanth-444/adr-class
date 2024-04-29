import numpy as np
import matplotlib.pyplot as  plt


class Visuals:
    def __init__(self) -> None:
        self.distance=[]
        self.angle_matrix=[]
        self.cordinates=[]

    def get_distance(self):
        return self.distance

    def set_distance(self, value):
        self.distance = value


    def get_visuals(self):
        self.angle_matrix=np.array(range(29,91,1))

        x= self.distance *np.sin(np.deg2rad(self.angle_matrix))
        y=self.distance* np.cos(np.deg2rad(self.angle_matrix))

        plt.clf()
        plt.scatter(x, y)
        plt.pause(0.001)
        plt.show()

if __name__== '__main__':

    visuals=Visuals()
        
    visuals.set_distance([1.2719975,1.2719975,0.3785381,0.36046386,0.35620683,0.356,0.36154813,0.36943758,0.38366827,0.38366827])
    visuals.get_visuals()
    