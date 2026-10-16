import numpy as np
import matplotlib.pyplot as plt

def f1(x):
    return x*x

def antiderivative(x):
    return (x**3) / 3

def diff(fun, h=1e-7):
    return lambda x: (fun(x+h) - fun(x-h))/2/h

n1=10
n2=15*n1

x = np.linspace(-np.pi, np.pi, n1)
fun = lambda x:np.abs(x)
y = fun(x)
fy = np.fft.fft(fun(x))
y1 = np.fft.ifft(fy)
fy_ = np.concatenate((fy, np.zeros(n2)))
print("::", fy_)
y2 = np.fft.ifft(fy_)*(n1+n2)/n1

plt.plot(x,y,'k+')
plt.plot(x,y1,'y.')
t = np.linspace(-np.pi, np.pi, len(y2))
plt.plot(t,y2,'r--',linewidth=4)

print(y)
print(y1)
plt.plot(x, y)
plt.show()
