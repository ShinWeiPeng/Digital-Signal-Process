import numpy as np
import matplotlib.pyplot as plt

A = 1
T = 2
w = np.linspace(-20, 20, 1000)
X = A * T * np.sinc(w * T / (2 * np.pi))

plt.plot(w, X)
plt.xlabel(r'$\omega$')
plt.ylabel(r'X($\omega$)')

plt.show()