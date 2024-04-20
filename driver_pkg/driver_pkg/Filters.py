import numpy as np
import matplotlib.pyplot as plt

class Filters:
    def __init__(self) -> None:
        pass
    def signal_smoothing_filter(matrix):
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
    plt.plot([5.29325226,5.24669921,0.21393563,5.0,5.17035209,5.15641116,0.15,5.15,5.15,5.15])
    plt.plot(Filters.gaussian_filter([5.29325226,5.24669921,0.21393563,5.0,5.17035209,5.15641116,0.15,5.15,5.15,5.15]))
    plt.show()