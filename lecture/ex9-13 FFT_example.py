import numpy as np
from numpy.fft import fft, ifft

x = np.array([1, 2, 4 , 3])
X = fft(x)
Xm = abs(X)
xx = ifft(X)

print("x = ", x)
print("X = ", X)
print("Magnitude of X = ", Xm)
print("Inverse FFT of X = ", xx)