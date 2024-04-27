import numpy as np
n=2
a = np.array([1,2,3,3,-1])
np.argsort(a)[-n:]
print(np.argsort(a)[-1:])