import numpy as np
import matplotlib.pyplot as plt
import control
wc = 2 * np.pi * 5
LPF = control.tf([wc], [1, wc])
w = np.logspace(-1.5,3,200)
fig, ax = plt.subplots(2, 1, figsize=(12, 8))
mag, phase, omega = control.bode(LPF, w, ax=ax, Hz=True, dB=False, deg=True, plot=True)
plt.show()