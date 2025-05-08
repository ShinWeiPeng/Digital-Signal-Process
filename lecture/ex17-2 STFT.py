import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pywt

# 設定參數
fs = 1000  # 取樣頻率
n = 256  # STFT 窗口大小

# 產生測試訊號
t = np.linspace(0, 10, fs * 10, endpoint=False)
x = np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 120 * t)  # 50Hz + 120Hz 訊號
# x = np.sin(2 * np.pi * 50 * t)

# 計算 STFT 頻譜
f_stft, t_stft, Zxx = signal.stft(x, fs, window='hann', nperseg=n)

wave_name = 'morl'
fc_wavelet = pywt.central_frequency(wave_name)
print(f"{wave_name} central frequency = {fc_wavelet}")

# 計算 CWT Scale 和對應頻率
cparam = 2 * fc_wavelet * n
scales = cparam / np.arange(n , 0, -1)

# 計算 CWT
cwt_matrix, frequencies = pywt.cwt(x, scales, wave_name, 1/fs)

# 繪製圖形
fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex='col')

ax[0].plot(t, x)
ax[0].set_title("Raw Data")
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("Amplitude")
ax[0].grid()

ax[1].pcolormesh(t_stft, f_stft, np.abs(Zxx), shading='gouraud')
ax[1].set_title("STFT Spectrogram")
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Frequency (Hz)")

ax[2].contourf(t, frequencies, np.abs(cwt_matrix))
ax[2].set_title("CWT Spectrogram")
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Frequency (Hz)")

fig.tight_layout()
plt.show()