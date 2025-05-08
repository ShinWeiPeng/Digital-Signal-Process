import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


print("Chebyshev Type II Filter Design")
print("(1)Lowpass Filter")
print("(2)Highpass Filter")
print("(3)Bandpass Filter")
print("(4)Bandstop Filter")

use_filter = eval(input("Plesase enter your choice: "))
print("-------------------------------------------")

filter_name = ['lowpass', 'highpass', 'bandpass', 'bandstop']


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
    
    n, wn = signal.cheb2ord(wp, ws, rp, abs(rs))
    b, a = signal.cheby2(n, rp, wn, filter_name[use_filter - 1])
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
    
    n, wn = signal.cheb2ord([wp1, wp2], [ws1, ws2], rp, abs(rs))
    b, a = signal.cheby2(n, rp, wn, filter_name[use_filter - 1])
else:
    print("Your choice is bot supproted!")
    quit()
    

print('IIR Filter Order = ', n)
print('IIR Filter Order = ', len(a) - 1)
print('IIR Filter Order = ', len(b) - 1)

w, H = signal.freqz(b, a)
magnitude = abs(H)
magnitude_db = 20 * np.log10(abs(H))
phase = np.angle(H)
phase_degree = np.degrees(np.angle(H))
freqs = w / np.pi * (Fs / 2)  # 轉換為 Hz

fig, ax = plt.subplots(2, 2, sharex='col')

ax[0, 0].plot(w, magnitude)
ax[0, 0].set_ylabel('Magnitude')
ax[0, 0].set_title(f'{filter_name[use_filter - 1].capitalize()} Chebyshev Type II Filter Response')
ax[0, 0].grid()

ax[1, 0].plot(w, phase)
ax[1, 0].set_xlabel(r'$\omega$ (2pi)')
ax[1, 0].set_ylabel('Phase (2pi)')
ax[1, 0].grid()

ax[0, 1].plot(freqs, magnitude_db)
ax[0, 1].set_ylabel('Magnitude (dB)')
ax[0, 1].set_title(f'{filter_name[use_filter - 1].capitalize()} Chebyshev Type II Filter Response')
ax[0, 1].grid()

ax[1, 1].plot(freqs, phase_degree)
ax[1, 1].set_xlabel('Frequency (Hz)')
ax[1, 1].set_ylabel('Phase (degree)')
ax[1, 1].grid()

fig.tight_layout()
plt.show()
