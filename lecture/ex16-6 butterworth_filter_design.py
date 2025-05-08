import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.signal import group_delay

print("Butterworth Filter Design")
print("(1)Lowpass Filter")
print("(2)Highpass Filter")
print("(3)Bandpass Filter")
print("(4)Bandstop Filter")

filter_name = {
    1: 'lowpass',
    2: 'highpass',
    3: 'bandpass',
    4: 'bandstop'
}

use_filter = eval(input("Plesase enter your choice: "))
print("-------------------------------------------")

if use_filter == 1 or use_filter == 2:
    fp = eval(input("Enter passband edge frequency(Hz): "))
    fs = eval(input("Enter stopband edge frequency(Hz): "))
    linear_rp = eval(input("Enter passband gain(linear): "))
    linear_rs = eval(input("Enter stopband gain(linear): "))
    Fs = eval(input("Enter sampleing frequency(Hz): "))
    
    wp = 2 * fp / Fs
    ws = 2 * fs / Fs
    
    print('fp = ', fp, '(Hz), ', 'wp = ', wp, '(rad)')
    print('fs = ', fs, '(Hz), ', 'ws = ', ws, '(rad)')
    
    rp = 20 * np.log10(linear_rp)
    rs = 20 * np.log10(linear_rs)
    
    print('linear_rp = ', linear_rp, '(magnification), ', 'rp = ', rp, '(dB)')
    print('linear_rs = ', linear_rs, '(magnification), ', 'rs = ', rs, '(dB)')
    
    n, wn = signal.buttord(wp, ws, rp, abs(rs))
    b, a = signal.butter(n, wn, filter_name[use_filter])
elif use_filter == 3 or use_filter == 4:
    fp1 = eval(input("Enter 1st passband edge frequency(Hz): "))
    fp2 = eval(input("Enter 2st passband edge frequency(Hz): "))
    fs1 = eval(input("Enter 1st stopband edge frequency(Hz): "))
    fs2 = eval(input("Enter 2st stopband edge frequency(Hz): "))
    linear_rp = eval(input("Enter passband gain(linear): "))
    linear_rs = eval(input("Enter stopband gain(linear): "))
    Fs = eval(input("Enter sampleing frequency(Hz): "))
    
    wp1 = 2 * fp1 / Fs
    wp2 = 2 * fp2 / Fs
    ws1 = 2 * fs1 / Fs
    ws2 = 2 * fs2 / Fs
    
    print('fp1 = ', fp1, '(Hz), ', 'wp1 = ', wp1, '(rad)')
    print('fs1 = ', fs1, '(Hz), ', 'ws1 = ', ws1, '(rad)')
    print('fp2 = ', fp2, '(Hz), ', 'wp2 = ', wp2, '(rad)')
    print('fs2 = ', fs2, '(Hz), ', 'ws2 = ', ws2, '(rad)')
    
    rp = 20 * np.log10(linear_rp)
    rs = 20 * np.log10(linear_rs)
    
    print('linear_rp = ', linear_rp, '(magnification), ', 'rp = ', rp, '(dB)')
    print('linear_rs = ', linear_rs, '(magnification), ', 'rs = ', rs, '(dB)')
    
    n, wn = signal.buttord([wp1, wp2], [ws1, ws2], rp, abs(rs))
    b, a = signal.butter(n, wn, filter_name[use_filter])
else:
    print("Your choice is bot supproted!")
    quit()
    
print('IIR Filter Order = ', n)
print('IIR Filter Order = ', len(a) - 1)
print('IIR Filter Order = ', len(b) - 1)

w, H = signal.freqz(b, a)
# magnitude = abs(H)
magnitude = 20 * np.log10(abs(H))
phase = np.degrees(np.angle(H))
freqs = w / np.pi * (Fs / 2)  # 轉換為 Hz

fig, ax = plt.subplots(3, 1, sharex=True)

ax[1].plot(freqs, magnitude)
ax[1].set_ylabel('Magnitude (dB)')
# ax[1].set_title(f'{filter_name[use_filter].capitalize()} Butterworth Filter Response')
ax[1].grid()

ax[0].plot(freqs, abs(H))
ax[0].set_ylabel('Magnitude')
ax[0].set_title(f'{filter_name[use_filter].capitalize()} Butterworth Filter Response')
ax[0].grid()

ax[2].plot(freqs, phase)
ax[2].set_xlabel('Frequency (Hz)')
ax[2].set_ylabel('Phase (degree)')
ax[2].grid()

fig.tight_layout()

FRAME_WIDE = 100
impulse = np.zeros(FRAME_WIDE)
impulse[3] = 1 
impulse_response = signal.lfilter(b, a, impulse)
point = np.arange(FRAME_WIDE)
t = point / Fs

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(t, impulse, label="Input", color='red')
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("Input")
# ax1.tick_params(axis='y', labelcolor='red')

# ax2 = ax1.twinx()
# ax2.plot(t, impulse_response, label="Output", color='blue')
# ax2.set_ylabel("Output", color='blue')
# ax2.tick_params(axis='y', labelcolor='blue')

ax1.plot(t, impulse_response, label="Output", color='blue')
ax1.set_ylabel("Output", color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')

ax1.grid()
ax1.set_title(f'{filter_name[use_filter].capitalize()} Impulse response')
# lines_1, labels_1 = ax1.get_legend_handles_labels()
# lines_2, labels_2 = ax1.get_legend_handles_labels()
# fig.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
# plt.legend(lines_1 + lines_2, labels_1 + labels_2)
plt.legend()
fig.tight_layout()

# 計算 group delay，並轉換成 Hz（因為 fs 有提供）
w_gd, gd = signal.group_delay((b, a), fs=Fs)
gd_ms = gd * 1000 / Fs  # 全部轉換為毫秒
# max_idx = np.argmax(gd)
# max_freq = w_gd[max_idx]
# max_delay = gd[max_idx]
# max_delay_ms = max_delay / Fs * 1000

# 畫出 Group Delay 圖
plt.figure(figsize=(10, 5))
plt.plot(w_gd, gd_ms, color='purple', label="Group Delay (ms)")
# plt.scatter([max_freq], [max_delay_ms], color='red', zorder=5,
#             label=f"Max Delay = {max_delay_ms:.2f} ms\n@ {max_freq:.1f} Hz")
# plt.axhline(0, color='gray', linestyle='--')
# plt.title("Highpass Group Delay")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Delay (ms)")
plt.grid(True)
# plt.legend()
plt.tight_layout()

plt.show()
