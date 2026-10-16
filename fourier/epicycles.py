import numpy as np
import pylab as plt
import matplotlib.animation as animation
from scipy.integrate import quad

def square(t):
    x = np.where(t < 0.5, np.minimum(0.25, t), np.maximum(0., 0.75 - t))
    y = np.where(t < 0.5, np.maximum(0., t - 0.25), np.minimum(0.25, 1.0 - t))
    return x + 1j * y

def heart(t):
    theta = t * 2 * np.pi
    x = 16 * np.sin(theta)**3
    y = 13 * np.cos(theta) - 5 * np.cos(2 * theta) - 2 * np.cos(3 * theta) - np.cos(4 * theta)
    return (x + 1j * y) / 16

def c_quad(f, a, b):
    return quad(lambda x: f(x).real, a, b)[0] + 1j * quad(lambda x: f(x).imag, a, b)[0]

def fourier(f, n):
    ks = np.arange(-n, n + 1)
    coeffs = np.zeros(2 * n + 1, dtype=complex)
    for i, k in enumerate(ks):
        ak = c_quad(lambda x: f(x) * np.exp(-1j * k * x), -np.pi, np.pi)
        coeffs[i] = ak / (2 * np.pi)
    
    order = np.argsort(np.abs(coeffs))[::-1]
    return ks[order], coeffs[order]

def fourier_sum(ks, coeffs, t):
    num_circles = len(coeffs)
    positions = np.zeros((num_circles + 1, 2, len(t)))
    radii = np.abs(coeffs)
    
    s = np.zeros(len(t), dtype=complex)
    for i, (k, ck) in enumerate(zip(ks, coeffs)):
        positions[i, 0, :] = s.real
        positions[i, 1, :] = s.imag
        s = s + ck * np.exp(1j * k * t)
        
    positions[-1, 0, :] = s.real
    positions[-1, 1, :] = s.imag
    return s, positions, radii

circle_count = 10
t = np.linspace(-np.pi, np.pi, 1000)

shape_fn = lambda x: heart((x + np.pi) / (2 * np.pi))
ks, cf = fourier(shape_fn, circle_count)
zf, positions, radii = fourier_sum(ks, cf, t)

pairs = shape_fn(np.linspace(-np.pi, np.pi, 200))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()
ax.set_aspect("equal")

ax.scatter(pairs.real, pairs.imag, c="b", s=10, alpha=0.3)
ax.plot(zf.real, zf.imag, "r-", linewidth=1)

circles = [plt.Circle((0, 0), radius=r, fill=False, color="gray", alpha=0.5) for r in radii]
for c in circles:
    ax.add_patch(c)

rod, = ax.plot([], [], "k-", linewidth=1)
point, = ax.plot([], [], "ro", markersize=6)

def init():
    rod.set_data([], [])
    point.set_data([], [])
    return circles + [rod, point]

def update(frame):
    for i, c in enumerate(circles):
        c.center = positions[i, :, frame]
        
    xs = positions[:, 0, frame]
    ys = positions[:, 1, frame]
    
    rod.set_data(xs, ys)
    point.set_data([xs[-1]], [ys[-1]])
    return circles + [rod, point]

step_size = 2
frames_to_render = range(0, len(t), step_size)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames_to_render,
    init_func=init,
    blit=False,
    interval=15
)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")
plt.show()