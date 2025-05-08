import numpy as np

x = np.array([1, 2, 4, 3, 2, 1, 1])
n0 = 2
y = x
for i in range(n0):
    y = np.insert(y, 0 ,0)
    
print(y)