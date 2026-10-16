import numpy as np
from numpy.fft import fft, ifft, fftshift, ifftshift
import matplotlib.pyplot as plt

def fourier_sum(coeffs, x):
    s = 0
    n = len(coeffs) // 2
    for k, ck in zip(range(-n, n+1), coeffs):
        print(k, ck)
        s += ck*np.exp(2*np.pi*k*1j*x)/len(coeffs)
    return s

sz = 1000
X = np.linspace(0, 1, sz)

n, m = 15, 15
t = np.arange(0 ,n)/n
y = np. sign (np. sin (t *2* np.pi) )
c_ = fftshift(fft(y))
print(c_)
c_ext = np.concatenate((np.zeros(m), c_, np.zeros(m)))
print(c_ext)
f_ = ifft(ifftshift(c_ext))
# print(f_)
f_ *= len(f_)//n


Z = fourier_sum(c_, X)

plt.plot(t, y, "k.", markersize=8)
plt.plot(X, Z, "b--")
plt.plot(np.linspace(0, 1, len(f_), endpoint=False), f_.real, "r-", linewidth=2, alpha=0.6)
plt.show()