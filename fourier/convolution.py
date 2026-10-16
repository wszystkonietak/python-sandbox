import numpy as np
from numpy.fft import fft, ifft, fftshift, ifftshift
# f = np.array([0, 0, 1, 2, 3,0,0])
f = np.array([1, 2, 0,0])
# g = np.array([0, 0, 0, 3, 2, 1, 0])
g = np.array([2,3,0,0])

gf = ifft(fft(f)*fft(g))

print(gf)