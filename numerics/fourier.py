import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

def fourier_sn(x, a0, an, bn):
    sum = a0
    for i, ai, bi in zip(range(len(an)), an, bn):
        sum+=ai*np.cos(i*x)+bi*np.sin(i*x)
    return sum

def fourier_sn_conv(fun, n):
    return lambda x: quad(lambda t: fun(x - t), )

def dn(x, n):
    return np.sin((n + 0.5) * x) / np.sin(x / 2)

def coefs(fun, N):
    a0 = quad(fun, 0, 2*np.pi)[0] / np.pi / 2
    an = [0]*N
    bn = [0]*N
    
    for i in range (N):
        an[i] = quad(lambda x: fun(x)*np.cos(i*x), 0, 2*np.pi)[0] / np.pi
        bn[i] = quad(lambda x: fun(x)*np.sin(i*x), 0, 2*np.pi)[0] / np.pi
    return a0, an, bn


x = np.linspace(-4 * np.pi, 4 * np.pi, 1000) 
fun = lambda x: np.sign(np.cos(x))
y = fun(x)
for i in range(35, 50, 5):
    a0, an, bn = coefs(fun, i)
    y2 = fourier_sn(x, a0, an, bn)
    plt.plot(x, y2, label=f"$sin_{i}(x)$")

plt.plot(x, y, label='sin(x)')
plt.ylim(-2, 2)
plt.grid(True)
# plt.legend()
plt.show()

