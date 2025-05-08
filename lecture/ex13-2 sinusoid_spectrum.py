import numpy as np
from numpy.fft import fft, fftshift, fftfreq
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 1000, endpoint = False)
x = np.cos(2 * np.pi * 100 * t)

X = fft((x))
Xm = abs(X)

f = fftshift(fftfreq(1000, 0.001))
X1 = fftshift(fft((x)))
X1m = abs(fftshift(fft((x))))

plt.figure(1)
plt.plot(Xm)
plt.xlabel('k')
plt.ylabel('Magnitude')

plt.figure(2)
plt.plot(f, X1m)
plt.xlabel('f')
plt.ylabel('Magnitude')

plt.show()
