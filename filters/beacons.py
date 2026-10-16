import numpy as np
import pylab as plt

np.random.seed(42)

def diffi_at_x(f, x, i, args=(), h=1e-6):
    h_ = np.zeros_like(x)
    h_[i] = h
    return (f(x + h_, *args) - f(x - h_, *args)) / (2.0 * h)

def jacobian_at_x(g, x, args=()):
    return np.array([
        diffi_at_x(g, x, i, args=args) for i in range(len(x))
    ]).T

def h(x, b):
    return np.sqrt((b[0] - x[0])**2 + (b[1] - x[1])**2 + (b[2] - x[2])**2)

beacons = np.random.uniform(-10.0, 10.0, size=(10, 3))

mean = np.array([0.0, 0.0, -8.0])
x_sim = mean.copy()
x_odom = mean.copy()
cov = np.eye(3) * 0.01

M = np.eye(3) * 0.08
Q = 0.25
A = np.eye(3)

N = 300
t = np.linspace(0, 4 * np.pi, N)
u = np.column_stack([
    0.25 * np.cos(t),
    0.25 * np.sin(2 * t),
    np.full(N, 16.0 / N)
])

simulation = []
odometry = []
estimation = []

for i in range(N):
    noise_u = np.random.multivariate_normal(np.zeros(3), M)
    x_sim = x_sim + u[i]
    x_odom = x_odom + u[i] + noise_u

    mean = mean + u[i] + noise_u
    cov = A.dot(cov).dot(A.T) + M

    for b in beacons:
        z_true = h(x_sim, b)
        z_noisy = z_true + np.random.normal(0, np.sqrt(Q))
        z_est = h(mean, b)

        H = jacobian_at_x(h, mean, args=(b,))
        S = H.dot(cov).dot(H.T) + Q
        K = cov.dot(H.T) / S

        mean = mean + K * (z_noisy - z_est)
        cov = (np.eye(3) - np.outer(K, H)).dot(cov)

    simulation.append(x_sim.copy())
    odometry.append(x_odom.copy())
    estimation.append(mean.copy())

simulation = np.array(simulation)
odometry = np.array(odometry)
estimation = np.array(estimation)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection="3d")

ax.scatter(beacons[:, 0], beacons[:, 1], beacons[:, 2], c="g", marker="^", s=60, label="beacons")
ax.plot(simulation[:, 0], simulation[:, 1], simulation[:, 2], "r-", linewidth=1.5, label="simulation")
ax.plot(estimation[:, 0], estimation[:, 1], estimation[:, 2], "b-", linewidth=1.2, label="ekf")
ax.plot(odometry[:, 0], odometry[:, 1], odometry[:, 2], "m--", linewidth=1, alpha=0.7, label="odometry")

ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_zlim(-12, 12)

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_zlabel("Z [m]")
ax.legend()
plt.show()