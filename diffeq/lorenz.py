import torch
import pylab as plt
import matplotlib.animation as animation
from torchdiffeq import odeint

def lorenz(t, y): 
    return torch.stack([
        10 * (y[1] - y[0]),
        y[0] * (28 - y[2]) - y[1],
        y[0] * y[1] - (8.0 / 3.0) * y[2]
    ])

t = torch.linspace(0, 200, 20000)

sol = odeint(lorenz, torch.tensor([[1., 1., 1.], [1., 1., 1.01]]).T, t)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection='3d')

ax.plot(sol[:, 0, 0], sol[:, 1, 0], sol[:, 2, 0], "r-", linewidth=0.1)
ax.plot(sol[:, 0, 1], sol[:, 1, 1], sol[:, 2, 1], "b-", linewidth=0.15)

point1, = ax.plot([], [], 'bo', markersize=10)
point2, = ax.plot([], [], 'ro', markersize=10)

def init():
    point1.set_data([], [])
    point1.set_3d_properties([])
    
    point2.set_data([], [])
    point2.set_3d_properties([])
    return point1, point2

def update(frame):
    x1 = sol[frame, 0, 0].item()
    y1 = sol[frame, 1, 0].item()
    z1 = sol[frame, 2, 0].item()

    x2 = sol[frame, 0, 1].item()
    y2 = sol[frame, 1, 1].item()
    z2 = sol[frame, 2, 1].item()

    point1.set_data([x1], [y1])
    point1.set_3d_properties([z1])
    
    point2.set_data([x2], [y2])
    point2.set_3d_properties([z2])
    
    return point1, point2

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

ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.set_zlabel("Z label")
plt.show()