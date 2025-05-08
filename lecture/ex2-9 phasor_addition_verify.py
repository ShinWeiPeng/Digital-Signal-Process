import numpy as np

phasor1 = complex(3 * np.cos(np.pi / 4), 3 * np.sin(np.pi / 4))
phasor2 = complex(4 * np.cos(3 * np.pi / 4), 4 * np.sin(3 * np.pi / 4))
phasor = phasor1 + phasor2
A = abs(phasor)
phi = np.angle(phasor)

print("phasor1 = ", phasor1)
print("phasor2 = ", phasor2)
print("phasor = ", phasor)
print("Magnitude = ", A)
print("Phase Angle = ", phi)