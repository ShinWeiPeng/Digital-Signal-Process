import numpy as np
import scipy.signal.windows as window
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

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
else:
    print("Your choice is bot supproted!")
    quit()

if filter_name[use_filter] == 'highpass' or filter_name[use_filter] == 'bandstop':
    print("設計 high-pass 或 band-stop 濾波器時 n（濾波器係數長度）需要為奇數，而 low-pass 和 band-pass 則不一定。")
    print("SciPy 的 firwin() 只能產生 Type I 與 Type II，也就是 對稱 FIR，Type I（奇數 taps）：支援所有通帶類型（LP/HP/BP/BS）、Type II（偶數 taps）：不能設計 High-pass / Band-stop")

numtaps = eval(input("Enter length of filter: "))
freq = eval(input("Enter sampleing frequency(Hz): "))

if filter_name[use_filter] == 'highpass' or filter_name[use_filter] == 'bandstop':
    if numtaps % 2 == 0:
        numtaps -= 1
        
print("-------------------------------------------")
print("Window function")
print("(1)Rectangular(Boxcar)")
print("(2)Hamming")
print("(3)Hanning")
print("(4)Bartlett")
print("(5)Blackman")
print("(6)Kaiser")
use_window = eval(input("Plesase enter your choice: "))

window_names = {
    1: 'boxcar', 
    2: 'hamming', 
    3: 'hanning', 
    4: 'bartlett', 
    5: 'blackman', 
    6: 'kaiser'
    }

if use_window <= 0 or use_window > 6:
    print("Your choice is bot supproted!")
    quit()
else:
    if use_window == 6:
        win = (window_names[use_window], 14)
    else:
        win = window_names[use_window]

if filter_name[use_filter] == 'lowpass':
    b = signal.firwin(numtaps, cutoff, window=win, pass_zero=True, fs=freq)
elif filter_name[use_filter] == 'highpass':
    b = signal.firwin(numtaps, cutoff, window=win, pass_zero=False, fs=freq)
elif filter_name[use_filter] == 'bandpass':
    b = signal.firwin(numtaps, [f1, f2], window=win, pass_zero=False, fs=freq)
else:
    b = signal.firwin(numtaps, [f1, f2], window=win, pass_zero=True, fs=freq)

print("FIR Filter Order:", len(b) - 1)

w, H = signal.freqz(b)
magnitude = 20 * np.log10(abs(H))
phase = np.degrees(np.angle(H))

ax = plt.subplot(3, 1, 1)  # 3x2 排列
cursor1 = Cursor(ax, useblit=True, color='green', linewidth=1)
plt.plot(w / np.pi * (freq / 2), magnitude)
plt.xlabel('Hz')
plt.ylabel('Magnitude')

ax = plt.subplot(3, 1, 2)  # 3x2 排列
cursor2 = Cursor(ax, useblit=True, color='red', linewidth=1)
plt.plot(w / np.pi * (freq / 2), phase)
plt.xlabel('Hz')
plt.ylabel('Phase')

# 計算時間點
n = np.arange(numtaps)
t = n - (numtaps - 1) / 2  # 中心點對齊

ax = plt.subplot(3, 1, 3)  # 3x2 排列
cursor3 = Cursor(ax, useblit=True, color='red', linewidth=1)
plt.plot(t, b, label="Windowed FIR (實際)")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.title('Impulse response')
plt.grid()

plt.tight_layout()
plt.show()
    

