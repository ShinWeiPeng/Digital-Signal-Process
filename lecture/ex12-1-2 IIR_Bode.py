import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

n = np.linspace(0, 10, 10, endpoint = False)
x = np.array([1, 2, 1, -1, -2, -1, 0, 0, 0, 0])

b = np.array([1])
a = np.array([1, -0.8])
y = signal.lfilter(b, a, x)
w, H = signal.freqz(b, a)

fs = 1000
magnitude_db = 20 * np.log10(abs(H))
phase_degree = np.degrees(np.angle(H))
freqs = w / np.pi * (fs / 2)  # 轉換為 Hz

print('n =', n)
print('x =', x)
print('y =', y)

fig, ax = plt.subplots(2, 2, figsize=(12, 8), sharex='col')

ax[0, 0].stem(n, x)
# ax[0, 0].set_xlabel('n')
ax[0, 0].set_ylabel('x[n]')

# plt.figure(1)
# plt.stem(n, x)
# plt.xlabel('n')
# plt.ylabel('x[n]')

ax[1, 0].stem(n, y)
ax[1, 0].set_xlabel('n')
ax[1, 0].set_ylabel('y[n]')

# plt.figure(2)
# plt.stem(n, y)
# plt.xlabel('n')
# plt.ylabel('y[n]')

ax[0, 1].plot(freqs, magnitude_db)
# ax[0, 1].set_xlabel('Frequency (Hz)')
ax[0, 1].set_ylabel('Magnitude (dB)')
ax[0, 1].grid()

ax[1, 1].plot(freqs, phase_degree)
ax[1, 1].set_xlabel('Frequency (Hz)')
ax[1, 1].set_ylabel('Phase (degree)')
ax[1, 1].grid()

fig.tight_layout()
plt.show()