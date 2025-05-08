import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

FRAME_WIDTH = 50
FREQUENCY = 1000
n = np.linspace(0, FRAME_WIDTH, FRAME_WIDTH, endpoint = False)
x = np.array([1, 2, 1, -1, -2, -1, 0, 0, 0, 0])
x = np.pad(x, (0, FRAME_WIDTH - len(x)), 'constant')

b = np.array([1])
a = np.array([1, -0.8])
y = signal.lfilter(b, a, x)


print('n =', n)
print('x =', x)
print('y =', y)

w, H = signal.freqz(b, a)
# magnitude = abs(H)
magnitude = 20 * np.log10(abs(H))
phase = np.degrees(np.angle(H))
freqs = w / np.pi * (FREQUENCY / 2)  # 轉換為 Hz

fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

ax[0].plot(freqs, abs(H))
ax[0].set_ylabel('Magnitude')
ax[0].set_title(f'Bode Plot')
ax[0].grid()

ax[1].plot(freqs, magnitude)
ax[1].set_ylabel('Magnitude (dB)')
# ax[1].set_title(f'{filter_name[use_filter].capitalize()} Butterworth Filter Response')
ax[1].grid()

ax[2].plot(freqs, phase)
ax[2].set_xlabel('Frequency (Hz)')
ax[2].set_ylabel('Phase (degree)')
ax[2].grid()

t = n / FREQUENCY
fig, ax1 = plt.subplots(figsize=(12, 8))

ax1.plot(t, x, label="Input x", color='red')
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("Input")
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.plot(t, y, label="Output y", color='blue')
ax2.set_ylabel("Output", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax1.set_title(f'Impulse response(Input v.s. Output)')
ax1.grid()
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
# fig.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
plt.legend(lines_1 + lines_2, labels_1 + labels_2)

plt.show()