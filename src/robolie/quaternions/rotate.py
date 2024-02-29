"""
Module for 3D rotations using quaternions

"""

from __future__ import annotations
from typing import Optional

import numpy as np

import robolie as rl


def rotate_by_quaternion(
    vector: np.ndarray,
    theta: Optional[float] = None,
    axis: Optional[np.ndarray] = None,
    quaternion: Optional[rl.Quaternion] = None,
) -> np.ndarray:
    """Rotates a vector by a quaternion.

    Args:
        vector: The vector to rotate.
        theta Optional[float]: The angle of rotation in radians.
        axis Optional[ndarray]: The axis of rotation as a 3D vector.
        quaternion Optional[Quaternion]: The quaternion representing the rotation.

    Returns:
        The rotated vector.
    """
    p: rl.Quaternion = rl.Quaternion(0, *vector)

    if quaternion is not None:
        q = quaternion
    else:
        assert np.isclose(np.linalg.norm(axis), 1), "The axis must be a unit vector."
        q: rl.Quaternion = rl.Quaternion.from_angle_and_axis(theta / 2, axis)

    q_conj: rl.Quaternion = q.conjugated()
    p_rot: rl.Quaternion = q * p * q_conj
    return p_rot.vector


def compute_average_rotation_quaternion(
    rotations: list[tuple[float, np.ndarray]]
) -> rl.Quaternion:
    """Computes the average of a set of 3D rotations, performed by queternions.

    Args:
        rotations: A list of rotations, each consisting of an angle and an axis.

    Returns:
        The average rotation as a Unit Quaternion.
    """

    # Convert rotations to quaternions
    quaternions = [
        rl.Quaternion.from_angle_and_axis(theta/2, axis) for theta, axis in rotations
    ]

    # Map all quaternions to the lie algebra
    pure_quaternions = [rl.log(q) for q in quaternions]

    # Compute the average pure quaternion
    average_pure_quaternion = rl.PureQuaternion(0, 0, 0)
    for i in range(len(pure_quaternions)):
        average_pure_quaternion += pure_quaternions[i]
    average_pure_quaternion = average_pure_quaternion / len(pure_quaternions)

    # Map the average pure quaternion back to the group using the exponential map
    average_quaternion = rl.exp(average_pure_quaternion)
    return average_quaternion
