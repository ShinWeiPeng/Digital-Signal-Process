import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
t = np.linspace(0, 1, 200, endpoint = False)
x = 10 * np.cos(2 * np.pi * 5 * t) + random.uniform(-5, 5, 200)
h = np.ones(7) / 7
y = np.convolve(x, h , 'same')

print(h)
# plt.figure(1)
plt.plot(t, x, '-', label = 'x(t)')
plt.plot(t, y, '-', label = 'x(t) filter')
plt.xlabel('t(second)')
plt.ylabel('Amplitude')

# plt.figure(2)
# plt.plot(t, y)
# plt.xlabel('t(second)')
# plt.ylabel('Amplitude')

plt.show()