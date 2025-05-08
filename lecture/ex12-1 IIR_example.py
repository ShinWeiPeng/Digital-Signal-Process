import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib import patches
import control
from matplotlib.ticker import LogFormatterExponent

def zplane(z, p):
    # fig = plt.figure()
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    unit_circle = patches.Circle((0, 0), radius = 1, fill = False, color = 'black', ls = 'dashed')
    ax.add_patch(unit_circle)
    plt.axvline(0, color = 'black')
    plt.axhline(0, color = 'black')
    plt.xlim((-2, 2))
    plt.ylim((-1.5, 1.5))
    plt.grid()
    plt.xlabel("R(實部)")
    plt.ylabel("I(虛部)")
    
    plt.plot(z.real, z.imag, 'go', fillstyle = 'none', ms = 10)
    plt.plot(p.real, p.imag, 'bx', fillstyle = 'none', ms = 10)
    return fig

print("Butterworth Filter Design")
print("(1)Lowpass Filter")
print("(2)Highpass Filter")
print("(3)Bandpass Filter")
print("(4)Bandstop Filter")

use_filter = eval(input("Plesase enter your choice: "))
print("-------------------------------------------")

filter_name = {
    1: 'lowpass', 
    2: 'highpass', 
    3: 'bandpass', 
    4: 'bandstop'
    }

if filter_name[use_filter] == 'lowpass' or  filter_name[use_filter] == 'highpass':
    fp = eval(input("Enter passband edge frequency(Hz): "))
    fs = eval(input("Enter stopband edge frequency(Hz): "))
    linear_rp = eval(input("Enter passband gain(linear): "))
    linear_rs = eval(input("Enter stopband gain(linear): "))
    Fs = eval(input("Enter sampleing frequency(Hz): "))
    
    wp = 2 * fp / Fs
    ws = 2 * fs / Fs
    
    if filter_name[use_filter] == 'lowpass':
        wc = 2 * np.pi * fp
        num = wc
        den = [1, wc]
        lpf = signal.TransferFunction(num, den)
        dt = 1 / Fs
        d_lpf = lpf.to_discrete(dt, method='gbt', alpha=0.5)
        G = control.tf(num, den)
        w = np.logspace(-1.5, 3, 200)
        mag, phase, omega = control.bode(G, w, Hz=True, dB=False, deg=True, plot=True)
        
    wp_range = wp
    ws_range = ws
    print('fp = ', fp, '(Hz), ', 'wp = ', wp, '(rad)')
    print('fs = ', fs, '(Hz), ', 'ws = ', ws, '(rad)')
    
    rp = 20 * np.log10(linear_rp)
    rs = 20 * np.log10(linear_rs)
    
    print('linear_rp = ', linear_rp, '(magnification), ', 'rp = ', rp, '(dB)')
    print('linear_rs = ', linear_rs, '(magnification), ', 'rs = ', rs, '(dB)')

elif filter_name[use_filter] == 'bandpass' or filter_name[use_filter] == 'bandstop':
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
    
    wp_range = [wp1, wp2]
    ws_range = [ws1, ws2]
    
    print('fp1 = ', fp1, '(Hz), ', 'wp1 = ', wp1, '(rad)')
    print('fs1 = ', fs1, '(Hz), ', 'ws1 = ', ws1, '(rad)')
    print('fp2 = ', fp2, '(Hz), ', 'wp2 = ', wp2, '(rad)')
    print('fs2 = ', fs2, '(Hz), ', 'ws2 = ', ws2, '(rad)')
    
    rp = 20 * np.log10(linear_rp)
    rs = 20 * np.log10(linear_rs)
    
    print('linear_rp = ', linear_rp, '(magnification), ', 'rp = ', rp, '(dB)')
    print('linear_rs = ', linear_rs, '(magnification), ', 'rs = ', rs, '(dB)')

else:
    print("Your choice is not supproted!")
    quit()

n, wn = signal.buttord(wp_range, ws_range, rp, abs(rs))
b, a = signal.butter(n, wn, filter_name[use_filter])
    
print('IIR Filter Order(via n) = ', n)
print('IIR Filter Order(via len(a)) = ', len(a) - 1)
print('IIR Filter Order(via len(b) = ', len(b) - 1)

w, H = signal.freqz(b, a)
# magnitude = abs(H)
magnitude = 20 * np.log10(abs(H))
phase = np.degrees(np.angle(H))
freqs = w / np.pi * (Fs / 2)  # 轉換為 Hz

fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

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

w, H = signal.freqz(d_lpf.num, d_lpf.den)
# magnitude = abs(H)
magnitude = 20 * np.log10(abs(H))
phase = np.degrees(np.angle(H))
freqs = w / np.pi * (Fs / 2)  # 轉換為 Hz

fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

ax[1].plot(freqs, magnitude)
ax[1].set_ylabel('Magnitude (dB)')
# ax[1].set_title(f'{filter_name[use_filter].capitalize()} Butterworth Filter Response')
ax[1].grid()

ax[0].plot(freqs, abs(H))
ax[0].set_ylabel('Magnitude')
ax[0].set_title(f'{filter_name[use_filter].capitalize()} Filter 1 Order Response')
ax[0].grid()

ax[2].plot(freqs, phase)
# ax[2].set_xlabel('Frequency (Hz)')
ax[2].set_ylabel('Phase (degree)')
ax[2].grid()

fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax[0].plot(freqs, abs(H))
ax[0].set_ylabel('Magnitude')
ax[0].set_title(f'{filter_name[use_filter].capitalize()} Filter 1 Order Response')
ax[0].grid()

ax[1].plot(freqs, phase)
ax[1].set_xlabel('Frequency (Hz)')
ax[1].set_ylabel('Phase (degree)')
ax[1].grid()

impulse = np.zeros(50)
impulse[0] = 1 

step = np.ones(50)
# step[0] = 0

impulse_response = signal.lfilter(b, a, impulse)
step_response = signal.lfilter(b, a, step)

fig, ax = plt.subplots(2, 1, figsize=(12, 8))
ax[0].stem(np.arange(len(impulse_response)), impulse_response, basefmt=" ")
ax[0].set_title(f'{filter_name[use_filter].capitalize()} IIR Impulse Response (via lfilter)')
ax[0].set_xlabel("n")
ax[0].set_ylabel("Amplitude")
ax[0].grid(True)

ax[1].stem(np.arange(len(step_response)), step_response, basefmt=" ")
ax[1].set_title(f'{filter_name[use_filter].capitalize()} IIR Step Response (via lfilter)')
ax[1].set_xlabel("n")
ax[1].set_ylabel("Amplitude")
ax[1].grid(True)

z, p, k = signal.tf2zpk(b, a)

fig_z = zplane(z, p)
fig_z.tight_layout()
fig.tight_layout()
plt.show()
