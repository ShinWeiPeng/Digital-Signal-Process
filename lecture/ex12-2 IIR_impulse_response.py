import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

n = np.linspace(0, 50, 50, endpoint = False)
x = np.zeros(len(n))
x[0] = 1

b = np.array([1])
a = np.array([1, -0.8])
y = signal.lfilter(b, a, x)


print('n =', n)
print('x =', x)
print('y =', y)


plt.figure(1)
plt.stem(n, x)
plt.xlabel('n')
plt.ylabel('x[n]')

plt.figure(2)
plt.stem(n, y)
plt.xlabel('n')
plt.ylabel('y[n]')

plt.show()