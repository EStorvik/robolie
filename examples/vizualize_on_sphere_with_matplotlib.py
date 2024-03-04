import matplotlib.pyplot as plt
import numpy as np

import robolie as rl

import time

# Define the initial point
p0 = np.array([0, -1, 0])

# Define the rotations
rotations = [
    (np.pi / 4, np.array([1, 0, 0])),
    (np.pi / 3, np.array([0, 1 / np.sqrt(2), 1 / np.sqrt(2)])),
    (np.pi / 2, np.array([0, 0, 1])),
]
labels = [f"Rotation {i+1}" for i in range(len(rotations))]


# compute average rotation
avg_quaternion = rl.compute_average_rotation_quaternion(rotations)
avg_angle, avg_axis = avg_quaternion.which_rotation()
rotations.append((avg_angle, avg_axis))
labels.append("Average Rotation")


def make_angles(angle, steps=100):
    return np.linspace(0, angle, steps)


# Initialize the figure
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Plot the paths
for i, (angle, axis) in enumerate(rotations):
    path = []
    p = p0.copy()
    angles = make_angles(angle)
    for angle in angles:
        rotated_point = rl.rotate_by_quaternion(p0, angle, axis)
        path.append(rotated_point)
    path = np.array(path)
    ax.plot(path[:, 0], path[:, 1], path[:, 2], label=labels[i])

# Add lines on the sphere
# u = np.linspace(0, 2 * np.pi, 10)
# v = np.linspace(0, np.pi, 10)
# x = np.outer(np.cos(u), np.sin(v))
# y = np.outer(np.sin(u), np.sin(v))
# z = np.outer(np.ones(np.size(u)), np.cos(v))
# ax.plot_wireframe(x, y, z, color='k', alpha=0.2)

# Add a sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, rstride=4, cstride=4, color="b", alpha=0.1)

# Add a 2D legend plot
ax2D = fig.add_axes([0.1, 0.8, 0.3, 0.1])
ax2D.axis("off")
ax2D.legend(
    handles=ax.get_legend_handles_labels()[0], labels=labels, loc="center", ncol=3
)


# Add labels and show the plot
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
