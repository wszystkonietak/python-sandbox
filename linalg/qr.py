import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import qr, det
sz = 100
x, y = np.meshgrid(np.linspace(0, 1, sz), np.linspace(0, 1, sz))
X = np.array([x.flatten(), y.flatten()])
a = np.array([[5,1], [3,4]])
c = np.array([[1,2], [0, 1]])
Q, R = qr(a)
Y = a.dot(X)
V = c.dot(X)
U = R.dot(X)
W = Q.dot(U)
print(Q)
print(R)
print(det(a))
print(det(c))
print(np.prod(np.diag(R)))
# U = R.dot()

plt.scatter(x, y)
plt.scatter(Y[0,:], Y[1,:], c='tab:orange')
plt.scatter(U[0,:], U[1,:], c='m')
plt.scatter(W[0,:], W[1,:], c='c')
print(np.degrees(np.atan2(Q[1,0],Q[0,0])))
# plt.scatter(Y[1,:], Y[0,:], c='tab:green')
plt.axis("square")
plt.show()