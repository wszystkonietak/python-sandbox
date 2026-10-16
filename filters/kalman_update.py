import numpy as np
import pylab as plt

np.random.seed(42)

def get_ellipse(mean, cov, n_std=2.0):
    vals, vecs = np.linalg.eigh(cov)
    theta = np.linspace(0, 2 * np.pi, 100)
    circle = np.vstack([np.cos(theta), np.sin(theta)])
    ellipse = vecs.dot(np.diag(n_std * np.sqrt(vals))).dot(circle)
    return ellipse[0] + mean[0], ellipse[1] + mean[1], vals, vecs

A = np.array([[1.0, 1.0], [0.0, 1.0]])
e = np.array([0.5, 1.0])
rho = 0.8
R = np.array([[e[0]**2, rho * e[0] * e[1]], [rho * e[0] * e[1], e[1]**2]])
Q = np.array([[10.0]])
C = np.array([[1.0, 0.0]])
z = np.array([5.0])

mean = np.array([0.0, 0.0])
cov = np.zeros((2, 2))

for i in range(1, 6):
    mean = A.dot(mean)
    cov = A.dot(cov).dot(A.T) + R

K = cov.dot(C.T).dot(np.linalg.inv(C.dot(cov).dot(C.T) + Q))
mean_post = mean + K.dot(z - C.dot(mean))
cov_post = (np.eye(2) - K.dot(C)).dot(cov)

Y_prior = np.random.multivariate_normal(mean, cov, 5000)
Y_post = np.random.multivariate_normal(mean_post, cov_post, 5000)

ex1, ey1, vals1, vecs1 = get_ellipse(mean, cov, n_std=2.0)
ex2, ey2, vals2, vecs2 = get_ellipse(mean_post, cov_post, n_std=2.0)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

ax.plot(Y_prior[:, 0], Y_prior[:, 1], "r.", markersize=2, alpha=0.15)
ax.plot(Y_post[:, 0], Y_post[:, 1], "b.", markersize=2, alpha=0.15)

ax.plot(ex1, ey1, "r--", linewidth=2, label="prior")
ax.plot(ex2, ey2, "b-", linewidth=2, label="posterior")
ax.axvline(z[0], color="g", linestyle="-.", linewidth=2, label="measurement")

for k in range(2):
    v_prior = vecs1[:, k] * 2.0 * np.sqrt(vals1[k])
    v_post = vecs2[:, k] * 2.0 * np.sqrt(vals2[k])
    ax.quiver(mean[0], mean[1], v_prior[0], v_prior[1], angles="xy", scale_units="xy", scale=1, color="darkred", width=0.006, zorder=5)
    ax.quiver(mean_post[0], mean_post[1], v_post[0], v_post[1], angles="xy", scale_units="xy", scale=1, color="navy", width=0.006, zorder=5)

ax.set_xlabel("X [m]")
ax.set_ylabel("V [m/s]")
ax.legend()
plt.show()