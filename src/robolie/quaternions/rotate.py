"""
Module for 3D rotations using quaternions

"""

from __future__ import annotations

import numpy as np

import robolie as rl


def rotate_by_quaternion(
    vector: np.ndarray, theta: float, axis: np.ndarray
) -> np.ndarray:
    """Rotates a vector by a quaternion.

    Args:
        vector: The vector to rotate.
        theta: The angle of rotation in radians.
        axis: The axis of rotation as a 3D vector.

    Returns:
        The rotated vector.
    """
    q: rl.Quaternion = rl.Quaternion.from_angle_and_axis(theta, axis)
    p: rl.Quaternion = rl.Quaternion(0, *vector)
    q_conj: rl.Quaternion = q.conjugated()
    p_rot: rl.Quaternion = q * p * q_conj
    return p_rot.vector
