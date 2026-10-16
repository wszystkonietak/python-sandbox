import numpy as np
import pylab as plt

def perceptron(X, Y):
    weights = np.random.randn(X.shape[1])
    bias = 0.0
    n = 0
    i = 0
    m = len(X)
    for _ in range(100000):
        if n >= m:
            break
        if Y[i] * (X[i].dot(weights) + bias) <= 0:
            weights += Y[i] * X[i]
            bias += Y[i]
            n = 0
        else:
            n += 1
        i = (i + 1) % m
    return weights, bias

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([-1, 1, 1, -1])

x3 = (X[:, 0] * X[:, 1]).reshape(-1, 1)
X_3d = np.hstack([X, x3])

weights, bias = perceptron(X_3d, Y)

nn = 50
xx1, xx2 = np.meshgrid(np.linspace(-0.5, 1.5, nn), np.linspace(-0.5, 1.5, nn))
zz = -(weights[0] * xx1 + weights[1] * xx2 + bias) / weights[2]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection='3d')

ax.plot_surface(xx1, xx2, zz, color='g', alpha=0.3)
ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2], c=Y, cmap='bwr', s=100, edgecolors='black')

ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-0.5, 1.5)
ax.set_zlim(-0.5, 1.5)

ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.set_zlabel("Z label")
plt.show()