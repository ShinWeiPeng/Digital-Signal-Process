import numpy as np
import scipy.signal.windows as window
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

M = 65

w = [
    window.boxcar(M),
    window.hamming(M),
    window.hann(M),
    window.bartlett(M),
    window.barthann(M),
    window.kaiser(M, 14)
]

plt.figure(figsize=(10, 8))

window_names = ['Boxcar', 'Hamming', 'Hann', 'Bartlett', 'Bartlett-Hann', 'Kaiser (β=14)']

for n in range(0, 5):
    plt.subplot(2, 3, n + 1)  # 3x2 排列
    plt.plot(w[n])
    plt.title(window_names[n])
    plt.xlabel('n')
    plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
