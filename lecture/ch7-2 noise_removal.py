import numpy as np
import numpy.random as random
import scipy.ndimage as signal
from scipy.signal import lfilter
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 200, endpoint = False)
x = 10 * np.cos(2 * np.pi * 5 * t) + random.uniform(-5, 5, 200)

h = np.ones(7) / 7
average_x = np.convolve(x, h , 'same')
print(h)

b = np.ones(7) / 7
fir_average = lfilter(b, 1, x)

# 產生 1D 高斯核
def gaussian(size, sigma):
    x = np.arange(-size, size + 1)
    kernel = np.exp(-x**2 / (2 * sigma**2))
    return kernel / np.sum(kernel)  # 正規化，使總和為 1

sigma = 3
filter_size = 6 * sigma + 1
gauss = gaussian(filter_size, sigma)
gauss_x = np.convolve(x, gauss, 'same')
print(gauss)

# plt.figure(1)
plt.legend(loc = 'upper right')
plt.plot(t, x, '-', label = 'x(t)')
plt.plot(t, average_x, '-', label = 'x(t) average filter')
plt.plot(t, gauss_x, '-', label = 'x(t) gauss filter')
plt.plot(t, fir_average, '-', label = 'x(t) fir_average')
plt.xlabel('t(second)')
plt.ylabel('Amplitude')

# plt.figure(2)
# plt.plot(t, y)
# plt.xlabel('t(second)')
# plt.ylabel('Amplitude')

plt.show()