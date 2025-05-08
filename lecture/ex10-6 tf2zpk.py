import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.markers import MarkerStyle

def zplane(z, p):
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)
    
    unit_circle = patches.Circle((0, 0), radius = 1, fill = False, color = 'black', ls = 'dashed')
    ax.add_patch(unit_circle)
    plt.axvline(0, color = 'black')
    plt.axhline(0, color = 'black')
    plt.xlim((-2, 2))
    plt.ylim((-1.5, 1.5))
    plt.grid()
    
    plt.plot(z.real, z.imag, 'go', fillstyle = 'none', ms = 10)
    plt.plot(p.real, p.imag, 'bx', fillstyle = 'none', ms = 10)
    return fig

def main():
    b = np.array([0.8, -0.16, -0.64])
    a = np.array([1, -0.2, -0.2, 1])
    z, p, k = signal.tf2zpk(b, a)
    
    print("Zero =", z)
    print("Poles =", p)
    print("Gain =", k)
    
    zplane(z, p)
    plt.show()
    return

main()
    
    