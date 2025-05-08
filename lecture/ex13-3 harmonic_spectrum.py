import numpy as np
from numpy.fft import fft, fftshift, fftfreq
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 1000, endpoint = False)
x = 10 + 10 * np.cos(2 * np.pi * 100 * t) + 2 * np.cos(2 * np.pi * 200 * t)

f = fftshift(fftfreq(1000, 0.001))
X = fftshift(fft(x))

Xm = abs(X)

plt.figure(1)
plt.plot(f, Xm)
plt.xlabel('f')
plt.ylabel('Magnitude')

plt.figure(2)
plt.plot(t, x)
plt.xlabel('t(second)')
plt.ylabel('Magnitude')

plt.show()
