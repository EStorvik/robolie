"""An Example where the log and exp maps are used to
compute the average of a set of 3D rotations, performed by queternions."""

from __future__ import annotations

import numpy as np

import robolie as rl

# Create list of rotations consisting of angles and axes
rotations = [
    (np.pi / 2, np.array([1, 0, 0])),
    (np.pi / 9, np.array([0, 1, 0])),
    (np.pi, np.array([0, 0, 1])),
]

# Convert rotations to quaternions
quaternions = [
    rl.Quaternion.from_angle_and_axis(theta / 2, axis) for theta, axis in rotations
]

# Map all quaternions to the lie algebra
pure_quaternions = [rl.log(q) for q in quaternions]

average_pure_quaternion = rl.PureQuaternion(0, 0, 0)
for i in range(len(pure_quaternions)):
    average_pure_quaternion += pure_quaternions[i]
average_pure_quaternion = average_pure_quaternion / len(pure_quaternions)


# Map the average pure quaternion back to the group
average_quaternion = rl.exp(average_pure_quaternion)

# Print axis and angle of the average quaternion
print(average_quaternion.which_rotation())
