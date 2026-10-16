import numpy as np
import pylab as plt
from scipy.integrate import quad

def square(t):
    
    x = np.where(t < 0.5, 
                 np.minimum(0.25, t), 
                 np.maximum(0., 0.75 - t))
    
    y = np.where(t < 0.5, 
                 np.maximum(0., t - 0.25), 
                 np.minimum(0.25, 1.0 - t))
    
    return x + 1j * y

def c_quad(f, a, b):
    return quad(lambda x: f(x).real, a, b)[0] + 1j*quad(lambda x: f(x).imag, a, b)[0]


def D(N, x):
    return np.sin(x*(N + .5))/(np.sin(x/2)+1e-100)

def S(N, x, f):
    return c_quad(lambda t: f(t)*D(N, x - t), -np.pi, np.pi)/2/np.pi

sum = S(50, 1, lambda x: square((x+np.pi)/2/np.pi))
print(sum)
t = np.linspace(-np.pi, np.pi, 1000)
y = np.array([S(10,x, lambda x: square((x+np.pi)/2/np.pi)) for x in t])
plt.plot(y.real, y.imag)
plt.show()