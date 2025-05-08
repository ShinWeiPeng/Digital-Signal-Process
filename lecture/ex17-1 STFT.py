import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pywt

print("Short-Time Fourier Transform")
n = eval(input("Enter the length of segment: "))  # STFT 區段長度
fs = eval(input("Enter the sampling frequency: "))  # 取樣頻率

# 產生時間軸
t = np.linspace(0, 1, fs)
t1 = np.linspace(0, 10, fs * 10, endpoint=False)  # 整個信號的時間範圍 (0~10s)

# 產生信號 (每 1 秒頻率遞增)
x = np.array([])
for i in range(10):
    segment = np.cos(2 * np.pi * ((i + 1) * 20) * t)  # 頻率從 20Hz 增加到 200Hz
    x = np.append(x, segment)

fig, ax = plt.subplots(4, 1, figsize=(12, 8), sharex='col')

# 1️⃣ **繪製原始信號**
ax[0].plot(t1, x)
# ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Amp')
ax[0].set_title(f"Raw Data")
ax[0].grid()

# 2️⃣ **STFT (短時傅立葉變換)**
f, t_stft, Zxx = signal.stft(x, fs, window='boxcar', nperseg=n)
ax[1].pcolormesh(t_stft, f, abs(Zxx), shading='auto')
ax[1].set_title('STFT')
# ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Frequency (Hz)')

# 3️⃣ **Spectrogram (SciPy 內建)**
f, t_spec, Zxx_spec = signal.spectrogram(x, fs)
ax[2].pcolormesh(t_spec, f, abs(Zxx_spec), shading='auto')
ax[2].set_title('SciPy Spectrogram')
# ax[2].set_xlabel('Time (s)')
ax[2].set_ylabel('Frequency (Hz)')

# 4️⃣ **CWT (連續小波轉換)**
wave_name = 'morl'
fc_wavelet = pywt.central_frequency(wave_name)
print(f"{wave_name} central frequency = {fc_wavelet}")

# 計算 CWT Scale 和對應頻率
cparam = 2 * fc_wavelet * n
scales = cparam / np.arange(n , 0, -1)

# 計算 CWT
cwt_matrix, frequencies = pywt.cwt(x, scales, wave_name, 1/fs)

ax[3].contourf(t1, frequencies, np.abs(cwt_matrix))
ax[3].set_title('CWT Spectrogram')
ax[3].set_xlabel('Time (s)')
ax[3].set_ylabel('Frequency (Hz)')

fig.tight_layout()
plt.show()