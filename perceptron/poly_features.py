import numpy as np
import pylab as plt
from sklearn.preprocessing import PolynomialFeatures

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

sz = 5
X1, X2 = np.meshgrid(np.linspace(-1, 1, sz), np.linspace(-1, 1, sz))
X = np.array([X1.flatten(), X2.flatten()]).T
Y = np.sign(np.random.randn(len(X)))
Y[Y == 0] = 1

poly = PolynomialFeatures(degree=5, include_bias=False)
V = poly.fit_transform(X)

weights, bias = perceptron(V, Y)

nn = 200
xx1, xx2 = np.meshgrid(np.linspace(-1.1, 1.1, nn), np.linspace(-1.1, 1.1, nn))
xx = np.array([xx1.flatten(), xx2.flatten()]).T
vv = poly.fit_transform(xx)
yy = (vv.dot(weights) + bias).reshape((nn, nn))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

ax.contourf(xx1, xx2, np.sign(yy), levels=[-1, 0, 1], cmap='bwr', alpha=0.3)
ax.contour(xx1, xx2, yy, levels=[0.0], colors='k', linewidths=1.5)
ax.scatter(X[:, 0], X[:, 1], c=Y, cmap='bwr', s=100, edgecolors='black')

ax.set_xlabel("X label")
ax.set_ylabel("Y label")
plt.show()