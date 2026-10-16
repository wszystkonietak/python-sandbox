import torch
import pylab as plt
import matplotlib.animation as animation
from torchdiffeq import odeint

g = 9.81
L = 1.
b = 0.5
A = 0.1
omega = 2.

def pendulum(t, y):
    angle_change = y[1]
    angle_change_change = -g / L * torch.sin(y[0]) - b * y[1] + A * torch.cos(omega * t)
    return torch.stack([angle_change, angle_change_change])

t = torch.linspace(0, 20, 4000)

sol = odeint(pendulum, torch.tensor([torch.pi, 0.]), t)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

ax.plot(torch.sin(sol[:, 0]), -torch.cos(sol[:, 0]), "r-", linewidth=0.1)

point, = ax.plot([], [], 'bo', markersize=10)
rod, = ax.plot([], [], 'k-', linewidth=2)

def init():
    point.set_data([], [])
    rod.set_data([], [])
    return point, rod

def update(frame):
    angle = sol[frame, 0]
    x = torch.sin(angle).item()
    y = -torch.cos(angle).item()

    point.set_data([x], [y])
    rod.set_data([0, x], [0, y])
    
    return point, rod

step_size = 5
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

ax.set_xlabel("X label")
ax.set_ylabel("Y label")
plt.show()