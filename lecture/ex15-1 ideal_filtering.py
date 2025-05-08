import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from numpy.fft import fft, ifft, fftshift, fftfreq

def ideal_lowpass_filter(x, cutoff, fs):
    X = fft(x)
    H = np.zeros(fs)
    for i in range(-cutoff, cutoff + 1):
        H[i] = 1
        
    Y = H * X
    y = ifft(Y)
    y = y.real
    return y

def ideal_highpass_filter(x, cutoff, fs):
    X = fft(x)
    H = np.zeros(fs)
    for i in range(-cutoff, cutoff + 1):
        H[i] = 1
        
    H = 1 - H
    Y = H * X
    y = ifft(Y)
    y = y.real
    return y

def ideal_bandpass_filter(x, cutoff, fs):
    if not isinstance(cutoff, (list, tuple)) or len(cutoff) != 2:
        raise ValueError("bandpass cutoff should be (low, high)")
    
    f1, f2 = cutoff
    X = fft(x)
    H = np.zeros(fs)
    for i in range(f1, f2 + 1):
        H[i] = 1
        
    for i in range(-f1, -f2 - 1, -1):
        H[i] = 1
        
    Y = H * X
    y = ifft(Y)
    y = y.real
    return y

def ideal_bandstop_filter(x, cutoff, fs):
    if not isinstance(cutoff, (list, tuple)) or len(cutoff) != 2:
        raise ValueError("bandpass cutoff should be (low, high)")
    
    f1, f2 = cutoff
    X = fft(x)
    H = np.zeros(fs)
    for i in range(f1, f2 + 1):
        H[i] = 1
        
    for i in range(-f1, -f2 - 1, -1):
        H[i] = 1
        
    H = 1 - H
    Y = H * X
    y = ifft(Y)
    y = y.real
    return y

def ideal_allpass_filter(x, *args):
    X = fft(x)
    Y = X
    y = ifft(Y)
    y = y.real
    return y

def main():
    print('DSP in Frequency Domanin')
    print('(1)Ideal Lowpass Filtering')
    print('(2)Ideal Highpass Filtering')
    print('(3)Ideal Bandpass Filtering')
    print('(4)Ideal Bandstop Filtering')
    print('(5)Ideal Allpass Filtering')

    ideal_filter = {
        1: ideal_lowpass_filter,
        2: ideal_highpass_filter,
        3: ideal_bandpass_filter,
        4: ideal_bandstop_filter,
        5: ideal_allpass_filter
    }

    filter_name = {
        1: 'lowpass',
        2: 'highpass',
        3: 'bandpass',
        4: 'bandstop',
        5: 'allpass'
    }
    
    choice = eval(input('Please enter your choice: '))
    if choice < 1 or choice > len(filter_name):
        print("Invalid choice!")
        exit()
    
    if filter_name[choice] == 'lowpass' or filter_name[choice] == 'highpass':
        fc = eval(input('Please enter cutoff frequency(Hz): '))
    elif filter_name[choice] == 'bandpass' or filter_name[choice] == 'bandstop':
        f1 = eval(input('Please enter frequency f1(Hz): '))
        f2 = eval(input('Please enter frequency f2(Hz): '))
        fc = [f1, f2]
    elif filter_name[choice] == 'allpass':
        fc = 0
    else:
        print("Invalid choice!")
        exit()
        
    FREQUENCY = 500
    t = np.linspace(0, 1, FREQUENCY, endpoint=False)
    x = np.cos(2 * np.pi * 10 * t) + np.cos(2 * np.pi * 20 * t) + np.cos(2 * np.pi * 30 * t)

    y = ideal_filter[choice](x, fc, FREQUENCY)

    f = fftshift(fftfreq(FREQUENCY, 1 / FREQUENCY))
    Xm = abs(fftshift(fft(x)))
    Ym = abs(fftshift(fft(y)))

    plt.subplot(4, 1, 1)
    plt.plot(x)
    plt.xlabel('t(second)')
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 2)
    plt.plot(f, Xm)
    plt.xlabel('f')
    plt.ylabel('Magnitude')

    plt.subplot(4, 1, 3)
    plt.plot(y)
    plt.xlabel('t(second)')
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 4)
    plt.plot(f, Ym)
    plt.xlabel('f')
    plt.ylabel('Magnitude')
    
    plt.tight_layout()
    plt.show()

main()

    