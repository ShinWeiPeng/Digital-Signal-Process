import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

FREQUENCY = 2000

x = np.array([1, 0, 0 , 0])
X = fft(x)
Xm = abs(X)
xx = ifft(X)

print("x = ", x)
print("X = ", X)
print("Magnitude of X = ", Xm)
print("Inverse FFT of X = ", xx)

plt.plot(Xm)
plt.show()
