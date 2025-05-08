import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from read_acc_csv import ReadAccCsv
import pywt
from dialog import InputNumber
import scipy.signal as signal

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

    # plt.subplots()
    # plt.plot(freqs, magnitude, '-')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Magnitude')
    return signal.filtfilt(b, a, data)

# === 頻率對應 ===
def dwt_freq_ranges(fs, levels):
    ranges = []
    for n in range(1, levels + 1):
        f_high = fs / 2**n
        f_low = fs / 2**(n + 1)
        ranges.append(f"{f_low:.2f}–{f_high:.2f} Hz")
    return ranges[::-1]  # D4~D1 順序


# === 小波分解並計算 D1~D4 能量 ===
def get_wavelet_energy(signal, wavelet, levels):
    coeffs = pywt.wavedec(signal, wavelet=wavelet, level=levels)
    energy = [np.sum(c**2) for c in coeffs[1:]]  # D1 ~ D4
    return energy[::-1]  # D4 ~ D1

print("Accel DWT Analysis")

freq_sample = InputNumber("Plesase enter your sample frequency: ")
if freq_sample == None:
    quit()
    
# === 讀取資料 ===
df_collision = ReadAccCsv.Read()
df_no_collision = ReadAccCsv.Read()

# === 提取 Z 軸資料 ===
z_collision = df_collision[ReadAccCsv.Key.ACC_Z.value]
z_no_collision = df_no_collision[ReadAccCsv.Key.ACC_Z.value]

z_collision_hp = highpass_filter(z_collision, freq_sample, 300)
z_no_collision_hp = highpass_filter(z_no_collision, freq_sample, 300)

# === 小波參數設定 ===
wavelet = 'db4'
level = 6

x_labels = dwt_freq_ranges(freq_sample, level)

energy_col = get_wavelet_energy(z_collision_hp, wavelet, level)
energy_nocol = get_wavelet_energy(z_no_collision_hp, wavelet, level)

# === 繪圖 ===
x = np.arange(len(x_labels))
bar_width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x - bar_width/2, energy_col, width=bar_width, label='Collision', color='orangered')
plt.bar(x + bar_width/2, energy_nocol, width=bar_width, label='No Collision', color='skyblue')

plt.xticks(x, x_labels)
plt.xlabel("Frequency Range (Hz)")
plt.ylabel("Wavelet Energy")
plt.title("Wavelet Energy Comparison by Frequency Band")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()