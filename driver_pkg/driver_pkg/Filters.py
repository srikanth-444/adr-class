import numpy as np
import matplotlib.pyplot as plt

class Filters:
    def __init__(self) -> None:
        pass
    def signal_smoothing_filter(self,matrix):
        mean=np.mean(matrix)
        std=np.mean(matrix)
        

        indicies=[]
        for i in range(len(matrix)) :        
            if matrix[i]<=mean+0.5*std:
                indicies.append(i)

                
            
            
        
        return(indicies)
    

if __name__== '__main__':

  

    plt.figure(figsize=(1,1))
    plt.plot([1.2719975,1.2719975,0.3785381,0.36046386,0.35620683,0.356,0.36154813,0.36943758,0.38366827,0.38366827])
    plt.plot(Filters.signal_smoothing_filter([1.2719975,1.2719975,0.3785381,0.36046386,0.35620683,0.356,0.36154813,0.36943758,0.38366827,0.38366827]))
    plt.show()