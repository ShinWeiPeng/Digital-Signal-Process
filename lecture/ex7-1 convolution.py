import numpy as np

x = np.array([1, 2, 4, 3, 2, 1, 1])
h = np.array([1, 2, 3, 1, 1])
kernel = h / np.linalg.norm(h)
y = np.convolve(x, h, 'full')
y1 = np.convolve(x, h, 'same')
y2 = np.convolve(x, kernel, 'full')
y3 = np.convolve(x, kernel, 'same')

print("x =", x)
print("h =", h)
print(f"kernel ={kernel}, normalize = {np.linalg.norm(h)}")
print("Full Convolution y =", y)
print("Convolution y1 =", y1)
print("Full Convolution y2 =", y2)
print("Convolution y3 =", y3)
