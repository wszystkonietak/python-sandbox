import numpy as np
import matplotlib.pyplot as plt

def derivative(fun, x):
    h = 0.1
    return (fun(x + h) - fun(x)) / h
def diff(fun, h=1e-7):
    return lambda x: (fun(x+h) - fun(x-h))/2/h

f = np.sin
df = diff(f)
d2f = diff(df)
x = np.linspace(0, 2 * np.pi, 1000)

y = derivative(np.sin, x)

plt.plot(x, y)
plt.plot(x, d2f(x), "green")
plt.plot(x, np.cos(x), "r--")
plt.title("Sine Wave")
plt.xlabel("x values (radians)")
plt.ylabel("$f(x)$, taylor(f)")

plt.grid(True)
plt.show()
