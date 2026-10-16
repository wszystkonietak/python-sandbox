import torch
import pylab as plt
import matplotlib.animation as animation
from torchdiffeq import odeint

g = 9.81

def two_body(t, y): 
    pos1 = y[0:3]
    vel1 = y[3:6]
    pos2 = y[6:9]
    vel2 = y[9:12]

    dif = pos2 - pos1
    norm = torch.norm(dif)
    direction = dif / norm
    inv = 1. / norm**2
    acc1 = g * direction * inv
    acc2 = -g * direction * inv
    return torch.cat([vel1, acc1, vel2, acc2])

t = torch.linspace(0, 20, 2000)

y0 = torch.tensor([
    -1.0,  0.0, -1.8,   # pos1
     0.0, -1.1,  0.35,  # vel1
     1.0,  0.0, -1.8,   # pos2
     0.0,  1.1,  0.01   # vel2
])

sol = odeint(two_body, y0, t)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection='3d')

ax.plot(sol[:, 0], sol[:, 1], sol[:, 2], "r-", linewidth=0.5)
ax.plot(sol[:, 6], sol[:, 7], sol[:, 8], "b-", linewidth=0.5)

point1, = ax.plot([], [], 'ro', markersize=10)
point2, = ax.plot([], [], 'bo', markersize=10)

def init():
    point1.set_data([], [])
    point1.set_3d_properties([])
    
    point2.set_data([], [])
    point2.set_3d_properties([])
    return point1, point2

def update(frame):
    x1 = sol[frame, 0].item()
    y1 = sol[frame, 1].item()
    z1 = sol[frame, 2].item()

    x2 = sol[frame, 6].item()
    y2 = sol[frame, 7].item()
    z2 = sol[frame, 8].item()

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

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.set_zlabel("Z label")
plt.show()