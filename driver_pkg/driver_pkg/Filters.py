import numpy as np
import matplotlib.pyplot as plt

class Filters:
    def __init__(self) -> None:
        pass
    def signal_smoothing_filter(self,matrix):
        mean=np.mean(matrix)
        std=np.mean(matrix)
        

        
        while True:
            for i in range(len(matrix)):
                if i==0:
                    matrix[i]=matrix[i+1]
                elif i==len(matrix)-1:
                    matrix[i]=matrix[i-1]
                    
                elif matrix[i]>=mean+2*std:
                    matrix[i]=(matrix[i-1]+matrix[i+1])/2
                
            if(mean-np.mean(matrix))<0.01:
                break
            mean=np.mean(matrix)
            std=np.std(matrix)
            
            
        
        return(matrix)
    

if __name__== '__main__':

  

    plt.figure(figsize=(1,1))
    plt.plot([0.29325226,0.24669921,0.21393563,5.0,0.17035209,0.15641116,0.15,0.15,0.15,0.15])
    plt.plot(Filters.signal_smoothing_filter([0.29325226,0.24669921,0.21393563,5.0,0.17035209,0.15641116,0.15,0.15,0.15,0.15]))
    plt.show()