import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
for width in range(2, 9, 2):
    A = 1
    T = width
    w = np.linspace(-20, 20, 1000)
    X = A * T * np.sinc(w * T / (2 * np.pi))
    plt.plot(w, X, label=width)

plt.xlabel(r'$\omega$')
plt.ylabel(r'X($\omega$)')
plt.grid()
plt.legend()

plt.show()