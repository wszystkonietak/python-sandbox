import numpy as np
import pylab as plt

np.random.seed(42)

g0 = 9.81
dt = 0.05
N = 250

def diffi_at_x(f, x, i, args=(), h=1e-6):
    h_ = np.zeros_like(x)
    h_[i] = h
    return (f(x + h_, *args) - f(x - h_, *args)) / (2.0 * h)

def jacobian_at_x(g, x, args=()):
    return np.array([
        diffi_at_x(g, x, i, args=args) for i in range(len(x))
    ]).T

def g(x, u):
    phi, theta, psi = x
    wx, wy, wz = u
    dphi = wx + wy * np.sin(phi) * np.tan(theta) + wz * np.cos(phi) * np.tan(theta)
    dtheta = wy * np.cos(phi) - wz * np.sin(phi)
    dpsi = wy * np.sin(phi) / np.cos(theta) + wz * np.cos(phi) / np.cos(theta)
    return x + dt * np.array([dphi, dtheta, dpsi])

def h(x):
    phi, theta, psi = x
    return g0 * np.array([
        -np.sin(theta),
        np.cos(theta) * np.sin(phi),
        np.cos(theta) * np.cos(phi)
    ])

t = np.linspace(0, N * dt, N)
u_true = np.column_stack([
    0.4 * np.cos(0.6 * t),
    0.3 * np.sin(0.4 * t),
    0.15 * np.ones(N)
])

x_sim = np.array([0.0, 0.0, 0.0])
x_odom = x_sim.copy()
mean = x_sim.copy()
cov = np.eye(3) * 0.01

R = np.eye(3) * 0.002
Q = np.eye(3) * 0.6
gyro_bias = np.array([0.05, -0.04, 0.03])

simulation = []
odometry = []
estimation = []
measurement = []

for i in range(N):
    x_sim = g(x_sim, u_true[i])
    u_meas = u_true[i] + gyro_bias + np.random.normal(0, 0.04, 3)
    x_odom = g(x_odom, u_meas)

    G = jacobian_at_x(g, mean, args=(u_meas,))
    mean = g(mean, u_meas)
    cov = G.dot(cov).dot(G.T) + R

    z = h(x_sim) + np.random.multivariate_normal(np.zeros(3), Q)
    phi_acc = np.arctan2(z[1], z[2])
    theta_acc = np.arctan2(-z[0], np.sqrt(z[1]**2 + z[2]**2))

    H = jacobian_at_x(h, mean)
    S = H.dot(cov).dot(H.T) + Q
    K = cov.dot(H.T).dot(np.linalg.inv(S))

    mean = mean + K.dot(z - h(mean))
    cov = (np.eye(3) - K.dot(H)).dot(cov)

    simulation.append(x_sim.copy())
    odometry.append(x_odom.copy())
    estimation.append(mean.copy())
    measurement.append([phi_acc, theta_acc])

simulation = np.array(simulation)
odometry = np.array(odometry)
estimation = np.array(estimation)
measurement = np.array(measurement)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

ax.plot(measurement[:, 0], measurement[:, 1], "g.", markersize=4, alpha=0.4, label="measurement")
ax.plot(simulation[:, 0], simulation[:, 1], "r-", linewidth=2, label="simulation")
ax.plot(estimation[:, 0], estimation[:, 1], "b-", linewidth=1.5, label="ekf")
ax.plot(odometry[:, 0], odometry[:, 1], "m--", linewidth=1.2, label="odometry")

ax.set_xlabel("Roll [rad]")
ax.set_ylabel("Pitch [rad]")
ax.legend()
plt.show()