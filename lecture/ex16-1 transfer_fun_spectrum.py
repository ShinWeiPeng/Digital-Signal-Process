import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

# 假設我們有一個轉移函數：
# H(z) = (0.2 + 0.5z^-1) / (1 - 0.2z^-1 + 0.8z^-2)

b = np.array([0.2, 0.5])       # 分子係數
a = np.array([1.0, -0.2, 0.8]) # 分母係數

# 決定 FFT 的點數（越多頻率越細）
N = 512

# 做 FFT（零補齊到 N 點）
B_fft = np.fft.fft(b, N)
A_fft = np.fft.fft(a, N)

# 頻率響應 = 分子 / 分母（點除）
H = B_fft / A_fft

fs = 1000
# 頻率軸（從 0 到 2π）
# freq = np.fft.fftfreq(N, d=1) * 2 * np.pi
freq = np.fft.fftfreq(N, d=1/fs)

# 只取前半段（0 到 π，實頻域）
half = slice(0, N//2)

# 畫圖（幅度與相位）
plt.figure(figsize=(12, 5))

plt.subplot(4, 1, 1)
plt.plot(freq, 20 * np.log10(np.abs(H)))
plt.ylabel('Magnitude (dB)')
plt.xlabel("Frequency (Hz)")
plt.title("fft element-wise division")
plt.grid()

plt.subplot(4, 1, 2)
plt.plot(freq[half], 20 * np.log10(np.abs(H[half])))
plt.ylabel('Magnitude (dB)')
plt.xlabel("Frequency (Hz)")
plt.title("fft element-wise division")
plt.grid()

plt.subplot(4, 1, 3)
w, h = freqz(b, a, worN=N)
freqs = w / np.pi * (fs / 2)  # 轉換為 Hz
plt.plot(freqs, 20 * np.log10(abs(h)))
plt.ylabel("Magnitude (dB)")
plt.xlabel("Frequency (Hz)")
plt.title("freqz")
plt.grid()

plt.subplot(4, 1, 4)
plt.plot(freq[half], np.angle(H[half]) * 2 * np.pi)
plt.ylabel('Phase (degree)')
plt.xlabel("Frequency (Hz)")
plt.grid()

plt.tight_layout()
plt.show()