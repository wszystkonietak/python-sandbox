import torch
import pylab as plt
import matplotlib.animation as animation
from torchdiffeq import odeint

g = 9.81
v0 = 20.
p0 = 0.

def gravity(t, y):
    position = y[1]
    velocity = torch.tensor(-g)
    return torch.stack([position, velocity])

t = torch.linspace(0, 5, 200)

sol = odeint(gravity, torch.tensor([p0, v0]), t)
analytical = -0.5 * g * t**2 + v0 * t + p0

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

ax.plot(t, sol[:, 0], "r-", linewidth=1.5)
ax.plot(t, analytical, "b--", linewidth=1.5)

point1, = ax.plot([], [], 'ro', markersize=10)
point2, = ax.plot([], [], 'bo', markersize=6)

def init():
    point1.set_data([], [])
    point2.set_data([], [])
    return point1, point2

def update(frame):
    time = t[frame].item()
    y_ode = sol[frame, 0].item()
    y_ana = analytical[frame].item()

    point1.set_data([time], [y_ode])
    point2.set_data([time], [y_ana])
    
    return point1, point2

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

ax.set_xlabel("X label")
ax.set_ylabel("Y label")
plt.show()