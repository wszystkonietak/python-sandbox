import numpy as np
import pylab as plt

np.random.seed(42)

def low_variance_sampler(particles, weights):
    M = len(particles)
    weights = weights / np.sum(weights)
    r = np.random.uniform(0, 1.0 / M)
    c = weights[0]
    i = 0
    new_particles = np.zeros_like(particles)
    for m in range(M):
        U = r + m / M
        while U > c:
            i += 1
            c += weights[i]
        new_particles[m] = particles[i]
    return new_particles

landmarks = np.array([[-8.0, -8.0], [-8.0, 8.0], [8.0, -8.0], [8.0, 8.0], [0.0, 0.0]])
M_particles = 400
N = 200

x_true = np.array([0.0, -6.0, 0.0])
x_odom = x_true.copy()
particles = np.random.multivariate_normal(x_true, np.diag([0.5, 0.5, 0.05]), size=M_particles)
sigma_z = 1.0

simulation = []
odometry = []
estimation = []

for t in range(N):
    v, omega = 0.35, 0.06
    x_true[2] += omega
    x_true[0] += v * np.cos(x_true[2])
    x_true[1] += v * np.sin(x_true[2])

    x_odom[2] += omega + np.random.normal(0, 0.02)
    x_odom[0] += (v + np.random.normal(0, 0.05)) * np.cos(x_odom[2])
    x_odom[1] += (v + np.random.normal(0, 0.05)) * np.sin(x_odom[2])

    particles[:, 2] += omega + np.random.normal(0, 0.03, M_particles)
    particles[:, 0] += (v + np.random.normal(0, 0.08, M_particles)) * np.cos(particles[:, 2])
    particles[:, 1] += (v + np.random.normal(0, 0.08, M_particles)) * np.sin(particles[:, 2])

    dists_true = np.linalg.norm(landmarks - x_true[:2], axis=1)
    z = dists_true + np.random.normal(0, sigma_z, len(landmarks))

    weights = np.ones(M_particles)
    for l_idx, lm in enumerate(landmarks):
        dists_p = np.linalg.norm(particles[:, :2] - lm, axis=1)
        weights *= np.exp(-0.5 * ((z[l_idx] - dists_p) / sigma_z)**2) + 1e-12

    particles = low_variance_sampler(particles, weights)
    est = np.mean(particles[:, :2], axis=0)

    simulation.append(x_true[:2].copy())
    odometry.append(x_odom[:2].copy())
    estimation.append(est.copy())

simulation = np.array(simulation)
odometry = np.array(odometry)
estimation = np.array(estimation)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()
ax.set_aspect("equal")

ax.scatter(landmarks[:, 0], landmarks[:, 1], c="g", marker="^", s=80, label="landmarks")
ax.plot(particles[:, 0], particles[:, 1], "c.", markersize=4, alpha=0.5, label="particles")
ax.plot(simulation[:, 0], simulation[:, 1], "r-", linewidth=1.5, label="simulation")
ax.plot(estimation[:, 0], estimation[:, 1], "b-", linewidth=1.5, label="particle filter")
ax.plot(odometry[:, 0], odometry[:, 1], "m--", linewidth=1, alpha=0.7, label="odometry")

ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.legend()
plt.show()