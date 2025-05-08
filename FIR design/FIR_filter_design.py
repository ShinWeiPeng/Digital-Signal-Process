import numpy as np
import scipy.signal.windows as window
import scipy.signal as signal
import matplotlib.pyplot as plt
from fir_design import FIR_Design

print("FIR filter design using the window method")
print("(1)Lowpass Filter")
print("(2)Highpass Filter")
print("(3)Bandpass Filter")
print("(4)Bandstop Filter")
use_filter = eval(input("Plesase enter your choice: "))

filter_name = {
    1: 'lowpass',
    2: 'highpass',
    3: 'bandpass',
    4: 'bandstop'
}
print("-------------------------------------------")

if filter_name[use_filter] == 'lowpass' or filter_name[use_filter] == 'highpass':
    cutoff = eval(input("Enter cutoff frequency(Hz): "))
elif filter_name[use_filter] == 'bandpass' or filter_name[use_filter] == 'bandstop':
    f1 = eval(input("Enter 1st cutoff frequency(Hz): "))
    f2 = eval(input("Enter 2st cutoff frequency(Hz): "))
    cutoff = [f1, f2]
else:
    print("Your choice is bot supproted!")
    quit()

if filter_name[use_filter] == 'highpass' or filter_name[use_filter] == 'bandstop':
    print("設計 high-pass 或 band-stop 濾波器時 n（濾波器係數長度）需要為奇數，而 low-pass 和 band-pass 則不一定。")
    print("SciPy 的 firwin() 只能產生 Type I 與 Type II，也就是 對稱 FIR，Type I（奇數 taps）：支援所有通帶類型（LP/HP/BP/BS）、Type II（偶數 taps）：不能設計 High-pass / Band-stop")

numtaps = eval(input("Enter length of filter: "))
freq = eval(input("Enter sampleing frequency(Hz): "))

compare_windows = {
    # 'boxcar': window.boxcar(numtaps),
    'hamming': window.hamming(numtaps),
    'hanning': window.hann(numtaps),
    'bartlett': window.bartlett(numtaps),
    'blackman': window.blackman(numtaps),
    'kaiser': window.kaiser(numtaps, 14)
}

plt.figure(figsize=(10, 6))
plt.title(f'{filter_name[use_filter].capitalize()} Window Comparison: Frequency Response')

b = FIR_Design.Order(numtaps, cutoff, filter_type=filter_name[use_filter], fs=freq)

w, h = signal.freqz(b)
mag = 20 * np.log10(np.abs(h) + 1e-12)  # 加 1e-12 防止 log(0)
freqs = w / np.pi * (freq / 2)
all_mag = [mag] 
plt.figure(1, figsize=(10, 5))
plt.plot(freqs, mag, label='original')
        
for name, win_fn in compare_windows.items():
    b_win = np.array(b) * win_fn
    # b_win /= np.sum(b_win)  # 正規化

    w, h = signal.freqz(b_win)
    freqs = w / np.pi * (freq / 2)
    mag = 20 * np.log10(np.abs(h) + 1e-12)  # 加 1e-12 防止 log(0)
    all_mag.append(mag)
    plt.plot(freqs, mag, label=name)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.grid()
plt.legend()
ymin = np.min(all_mag)
ymax = np.max(all_mag)
padding = (ymax - ymin) * 0.1  # 給上下加10%的邊界
plt.ylim(ymin - padding, ymax + padding)
plt.tight_layout()

# 計算時間點
n = np.arange(numtaps)
t = n - (numtaps - 1) / 2  # 中心點對齊

plt.figure(2, figsize=(10, 5))
plt.plot(t, b)
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.title(f'{filter_name[use_filter].capitalize()} Impulse response(via b Coefficient(Zero))')
plt.grid()

impulse = np.zeros(len(b))
impulse[10] = 1 
impulse_response = signal.lfilter(b, 1.0, impulse)
n = np.arange(len(b))
t_center = (n - (len(b) - 1) / 2) / freq
t = n / freq

plt.figure(3, figsize=(10, 5))
# plt.stem(t, impulse_response, basefmt=" ")
plt.stem(t_center, impulse_response[:len(b)])
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title(f'{filter_name[use_filter].capitalize()} Impulse response(via lfilter)')
plt.grid()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(t, impulse, label="Input", color='red')
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("Input")
ax1.tick_params(axis='y', labelcolor='red')
# ax1.axvline(100, color='red', linestyle=':', label='Collision Time (n=0)')
# plt.legend()

ax2 = ax1.twinx()
ax2.plot(t, impulse_response, label="Output", color='blue')
ax2.set_ylabel("Output", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax1.set_title(f'{filter_name[use_filter].capitalize()} Impulse response(Input v.s. Output)')
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
# fig.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
plt.legend(lines_1 + lines_2, labels_1 + labels_2)

plt.show()

    

