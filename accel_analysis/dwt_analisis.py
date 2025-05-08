import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from read_acc_csv import ReadAccCsv
import pywt
from dialog import InputNumber
import scipy.signal as signal
from dwt_setting import DWT_Setting

HIGHPASS_FREQUENCY_TORRANCE = 1
RIPPLE_LINEAR = 0.02

# 設定 bandpass 濾波器：5~300 Hz
def highpass_filter(data, fs, cut=5):
    nyq = 0.5 * fs  # 奈奎斯特頻率
    if cut <= HIGHPASS_FREQUENCY_TORRANCE:
        ws = 1 / nyq
    else:
        ws = (cut - HIGHPASS_FREQUENCY_TORRANCE) / nyq
        
    wp = cut / nyq
    
    rp = 20 * np.log10(1 + RIPPLE_LINEAR)
    rs = 20 * np.log10(RIPPLE_LINEAR)
    
    n, wn = signal.ellipord(wp, ws, rp, abs(rs))
    b, a = signal.ellip(n, rp, abs(rs), wn, 'highpass')
    print(f"IIR Filter Order = {n}")

    w, H = signal.freqz(b, a)
    
    phase = np.degrees(np.angle(H))
    magnitude = abs(H)
    freqs = w / np.pi * (fs / 2)  # 轉換為 Hz

    return signal.filtfilt(b, a, data)

# === 頻率對應 ===
def dwt_freq_ranges(fs, levels):
    ranges = []
    for n in range(1, levels + 1):
        f_high = fs / 2**n
        f_low = fs / 2**(n + 1)
        ranges.append(f"{f_low:.2f}–{f_high:.2f}")
        
    ranges.append(f"0.0–{f_low:.2f}")
    return ranges[::-1] # 低頻到高頻順序

# === 小波分解並計算低頻至高頻能量 ===
def get_wavelet_energy(signal, wavelet, levels):
    coeffs = pywt.wavedec(signal, wavelet, level=levels)
    energy = [np.sum(c**2) for c in coeffs]  # 低頻->高頻
    return energy

def run_analysis(frequency_sample):
    csv_data = ReadAccCsv.Read()

    if csv_data == None:
        return None
    
    bar_width = 0.1
    x_labels = dwt_freq_ranges(frequency_sample, DWT_Setting.Level)
    x = np.arange(len(x_labels))
    
    # Create a grid of subplots
    fig = plt.figure(figsize=(12, 8))  # Adjust the figsize as needed
    fig.canvas.manager.set_window_title(f"{csv_data['FileName']} CWT Analysis")

    for axis_data in ReadAccCsv.Keys:
        if axis_data == ReadAccCsv.Key.FILE_NAME.value:
            break
        
        high_pass_data = highpass_filter(csv_data[axis_data], frequency_sample, 300)
        energy = get_wavelet_energy(high_pass_data, DWT_Setting.WaveletName, DWT_Setting.Level)
        
        if axis_data == ReadAccCsv.Key.ACC_X.value:
            plt.bar(x - bar_width, energy, width = bar_width, label='x-axis', color='skyblue')
        elif axis_data == ReadAccCsv.Key.ACC_Y.value:
            plt.bar(x, energy, width = bar_width, label='y-axis', color='orangered')
        else:
            plt.bar(x + bar_width, energy, width = bar_width, label='z-axis', color='black')

    plt.xlabel("Frequency Range (Hz)")
    plt.ylabel("Wavelet Energy")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    # plt.title(f"{csv_data['FileName']} CWT Analysis")
    plt.xticks(x, x_labels)  # Optionally rotate labels for better clarity
    print(f"{csv_data['FileName']} Analysis Finish")
    plt.legend(loc='upper left')
    fig.tight_layout()
    return True

print("Accel DWT Analysis")

freq_sample = InputNumber("Plesase enter your sample frequency: ")
if freq_sample == None or freq_sample <= 0:
    quit()

DWT_Setting.ChoiceDialog()

while run_analysis(freq_sample) != None:
    continue

print(f"Finish")
plt.show()
