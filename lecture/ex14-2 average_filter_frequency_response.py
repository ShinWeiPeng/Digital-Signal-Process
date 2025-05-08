import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from matplotlib.widgets import Cursor

Fs = 1000

filter_size = eval(input("please enter the filter size: "))
h = np.ones(filter_size) / filter_size

w, H = signal.freqz(h)
mag = abs(H)

# 產生 1D 高斯核
def gaussian(size, sigma):
    x = np.arange(-size, size + 1)
    kernel = np.exp(-x**2 / (2 * sigma**2))
    return kernel / np.sum(kernel)  # 正規化，使總和為 1

sigma = eval(input("please enter sigma: "))
filter_size_sigma = int(6 * sigma + 1)
gauss = gaussian(filter_size_sigma, sigma)

w_gauss, H_gauss = signal.freqz(gauss)
mag_gauss = abs(H_gauss)


# fig, ax = plt.subplots()
# cursor1 = Cursor(ax, useblit=True, color='red', linewidth=1)

# plt.figure(1)
# plt.plot(w, mag)
# plt.xlabel(r'$\omega$')
# plt.ylabel('Magnitude')

fig, ax = plt.subplots()
cursor1 = Cursor(ax, useblit=True, color='red', linewidth=1)

plt.figure(1)
plt.plot(w / np.pi * (Fs / 2), mag_gauss)  # 轉換為 Hz
plt.title('Gauss')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

fig, ax = plt.subplots()
cursor2 = Cursor(ax, useblit=True, color='green', linewidth=1)

plt.figure(2)
plt.plot(w / np.pi * (Fs / 2), mag)  # 轉換為 Hz
plt.title('Average')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')




plt.show()

