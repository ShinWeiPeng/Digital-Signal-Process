import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from numpy.fft import fft, ifft

Fs = 1000  # 假設採樣率 1000 Hz
filter_size = eval(input("please enter the filter size(odd): "))
filter_half = int(filter_size / 2)
wc = np.pi / 2
fc = eval(input("please enter the cutoff frequency: "))
# wc = 2 * np.pi / fc
print(f"wc = {wc}")
print('filter_size = ', filter_size, ', filter_half = ', filter_half)

na = np.arange(-filter_half, filter_half + 1)
h = np.zeros(filter_size)

for n in na:
    if n == 0:
        h[n + filter_half] = 0.5
    else:
        h[n + filter_half] = np.sin(wc * n) / (np.pi * n)

w, H = signal.freqz(h)
mag = abs(H)

H_fft = fft(h)
mag_fft = abs(H_fft)

# print('w = ', w, 'H = ', H)
plt.figure(1)
plt.stem(na, h)
plt.xlabel('n')
plt.ylabel('h[n]')

plt.figure(2)
plt.plot(w, mag)
plt.xlabel(r'$\omega$')
plt.ylabel('Magnitude')

freq = np.fft.fftfreq(len(h), d=1/Fs)
half = slice(0, len(h)//2)

plt.figure(4)
plt.subplot(2, 1, 1)
plt.plot(freq, mag_fft)
plt.title('FFT')
plt.xlabel("Frequency (Hz)")
plt.ylabel('Magnitude')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(freq[half], mag_fft[half])
plt.xlabel("Frequency (Hz)")
plt.ylabel('Magnitude')
plt.grid()

plt.figure(3)
plt.plot(w / np.pi * (Fs / 2), mag)  # 轉換為 Hz
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('freqz')

plt.tight_layout()
plt.show()
