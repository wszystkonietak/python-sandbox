import numpy as np
import matplotlib.pyplot as plt

def dsin(x, k):
    a = k % 4
    return np.sin(a*(np.pi /2) + x)

def taylor(x, k):
    sum = dsin(0, 0)
    a = 1
    for n in range(1, k + 1):
        a *= x / n
        sum += dsin(0, n)*a
    return sum


x = np.linspace(-4 * np.pi, 4 * np.pi, 1000) 
y = np.sin(x)
for i in range(1, 20):
    y2 = taylor(x, i)
    plt.plot(x, y2, label=f"$sin_{i}(x)$")

plt.plot(x, y, label='sin(x)')
plt.ylim(-2, 2)
plt.grid(True)
# plt.legend()
plt.show()

