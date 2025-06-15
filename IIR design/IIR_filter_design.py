import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.signal import group_delay
from dialog import InputNumber

count = 0
def run_analysis():
    global count
    count += 1
    print("(1)Butterworth Filter")
    print("(2)Elliptic Filter")
    print("(3)Chebyshev Type I Filter")
    print("(4)Chebyshev Type II Filter")
    
    used_filter_method = InputNumber("Plesase enter your choice: ")

    filter_design_method = {
        1: 'Butterworth',
        2: 'Elliptic',
        3: 'Chebyshev Type I',
        4: 'Chebyshev Type II'
    }
    
    if used_filter_method == None or used_filter_method > len(filter_design_method):
        print("Your choice is bot supproted!")
        return None
    
    print("-------------------------------------------")
    
    filter_order = {
        1: signal.buttord,
        2: signal.ellipord,
        3: signal.cheb1ord,
        4: signal.cheb2ord
    }

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
    
    used_filter = InputNumber("Plesase enter your choice: ")
    if used_filter == None or used_filter > len(filter_name):
        print("Your choice is bot supproted!")
        return None
    
    print("-------------------------------------------")

    if filter_name[used_filter] == 'lowpass' or filter_name[used_filter] == 'highpass':
        fp = InputNumber("Enter passband edge frequency(Hz): ")
        if fp == None:
            return None
        
        fs = InputNumber("Enter stopband edge frequency(Hz): ")
        if fs == None:
            return None
        
        linear_rp = InputNumber("Enter passband gain(linear): ")
        if linear_rp == None:
            return None
        
        linear_rs = InputNumber("Enter stopband gain(linear): ")
        if linear_rs == None:
            return None
        
        Fs = InputNumber("Enter sampleing frequency(Hz): ")
        if Fs == None:
            return None
        
        wp = 2 * fp / Fs    # (radians/sample), w = 2 * pi * f / Fs, w_normalized = w / pi = 2 * f / Fs
        ws = 2 * fs / Fs
            
        wp_range = [wp]
        ws_range = [ws]
        
        print('fp = ', fp, '(Hz), ', 'wp = ', wp, '(rad)')
        print('fs = ', fs, '(Hz), ', 'ws = ', ws, '(rad)')
        
        rp = 20 * np.log10(linear_rp)
        rs = 20 * np.log10(linear_rs)
        
        print('linear_rp = ', linear_rp, '(magnification), ', 'rp = ', rp, '(dB)')
        print('linear_rs = ', linear_rs, '(magnification), ', 'rs = ', rs, '(dB)')

    elif filter_name[used_filter] == 'bandpass' or filter_name[used_filter] == 'bandstop':
        fp1 = InputNumber("Enter 1st passband edge frequency(Hz): ")
        if fp1 == None:
            return None
        
        fp2 = InputNumber("Enter 2st passband edge frequency(Hz): ")
        if fp2 == None:
            return None
        
        fs1 = InputNumber("Enter 1st stopband edge frequency(Hz): ")
        if fs1 == None:
            return None
        
        fs2 = InputNumber("Enter 2st stopband edge frequency(Hz): ")
        if fs2 == None:
            return None
        
        linear_rp = InputNumber("Enter passband gain(linear): ")
        if linear_rp == None:
            return None
        
        linear_rs = InputNumber("Enter stopband gain(linear): ")
        if linear_rs == None:
            return None
        
        Fs = InputNumber("Enter sampleing frequency(Hz): ")
        if Fs == None:
            return None
        
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
        print("Your choice is bot supproted!")
        return None
    
    n, wn = filter_order[used_filter_method](wp_range, ws_range, rp, abs(rs))
    match filter_design_method[used_filter_method]:
        case 'Butterworth':
            b, a = signal.butter(n, wn, filter_name[used_filter])
        case 'Elliptic':
            b, a = signal.ellip(n, rp, abs(rs), wn, filter_name[used_filter])
        case 'Chebyshev Type I':
            b, a = signal.cheby1(n, rp, wn, filter_name[used_filter])
        case 'Chebyshev Type II':
            b, a = signal.cheby2(n, rp, wn, filter_name[used_filter])
        case _:
            raise NotImplementedError(f"'{used_filter_method}' not supported.")

    print(f'Number {count} IIR Filter {filter_design_method[used_filter_method]} {n} Order')
    print(f'Number {count} IIR Filter b Coefficients = {b}')
    print(f'Number {count} IIR Filter a Coefficients = {a}')
    
    print("-------------------------------------------")

    fig, ax = plt.subplots(3, 1, figsize=(8, 6))
    
    w, H = signal.freqz(b, a)
    magnitude = abs(H)
    # magnitude = 20 * np.log10(abs(H))
    phase = np.degrees(np.angle(H))
    freqs = w / np.pi * (Fs / 2)  # 轉換為 Hz

    ax[0].plot(freqs, magnitude)
    ax[0].set_ylabel('Magnitude')
    ax[0].set_title(f'{count} {filter_design_method[used_filter_method]} {filter_name[used_filter].capitalize()} {n} Order Filter')
    ax[0].grid()
    
    FRAME_WIDE = 200
    impulse = np.zeros(FRAME_WIDE)
    impulse[0] = 1 
    impulse_response = signal.lfilter(b, a, impulse)
    point = np.arange(FRAME_WIDE)
    t = point / Fs

    ax[1].plot(t, impulse, label="Input", color='red')
    ax[1].set_xlabel("Time(s)")
    ax[1].set_ylabel("Amplitude")

    ax[1].plot(t, impulse_response, label="Output", color='blue')
    ax[1].grid()
    ax[1].set_title(f'{count} {filter_design_method[used_filter_method]} {filter_name[used_filter].capitalize()} Impulse response')

    ax[1].legend()
    
    # 計算 group delay，並轉換成 Hz（因為 fs 有提供）
    w_gd, gd = signal.group_delay((b, a), fs=Fs)
    gd_ms = gd * 1000 / Fs  # 全部轉換為毫秒
    # 畫出 Group Delay 圖
    ax[2].plot(w_gd, gd_ms, color='purple', label="Group Delay (ms)")
    ax[2].set_title(f'{count} {filter_design_method[used_filter_method]} {filter_name[used_filter].capitalize()} Group Delay')
    ax[2].set_xlabel("Frequency (Hz)")
    ax[2].set_ylabel("Delay (ms)")
    ax[2].grid(True)
    
    fig.tight_layout()
    
    return True

print("IIR Filter Design")
while run_analysis() != None:
    continue

print(f"Finish")
plt.show()
