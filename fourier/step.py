import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def step(x):
    x = np.asarray(x)
    return np.sign(x)
    # return ((x % 1) < .5)

# def step(x):
    # x = np.asarray(x)
    # return np.abs(x)

def c_quad(f, a, b):
    return quad(lambda x: np.real(f(x)), a, b)[0] + 1j*quad(lambda x: np.imag(f(x)), a, b)[0]


def fourier(f, n):
    a = np.zeros(2*n+1, dtype=complex)
    for k in range(-n, n+1):
        # ak = quad(lambda x: f(x)*np.cos(-k*x), -np.pi, np.pi)[0] + 1j*quad(lambda x: f(x)*np.sin(-k*x), -np.pi, np.pi)[0]
        ak = c_quad(lambda x: f(x)*np.exp(-1j*k*x), -np.pi, np.pi)
        a[n+k] = ak/(2*np.pi)
        print(k, a[n+k])  
    return a

def fourier_sum(coeffs, x):
    s = 0
    n = len(coeffs) // 2
    for k, ck in zip(range(-n, n+1), coeffs):
        print(k, ck)
        s += ck*np.exp(k*1j*x)
    return s

sz = 1000
X = np.linspace(-np.pi, np.pi, sz)

Y = step(X)
coeffs = fourier(step, 50)
Z = fourier_sum(coeffs, X)
plt.plot(X, Y)
plt.plot(X, Z)
plt.show()