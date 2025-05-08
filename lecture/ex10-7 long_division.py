import numpy as np

b = np.array([1, 1, 2, -1, 3])
a = np.array([1, -1, 1, 0, 0])

M = b.size
N = a.size

x = np.zeros(M)
x[0] = b[0] / a[0]

for n in range(1, M):
    sum = 0
    k = n
    
    if n > n:
        k = N
        
    for i in range(1, k + 1):
        sum = sum + x[n - 1] * a[i]
        
    print(sum)
    x[n] = (b[n] - sum) / a[0]

print(x)    