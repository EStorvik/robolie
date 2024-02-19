"""Module for quaternions and operations on them."""

from __future__ import annotations

import numpy as np


class Quaternion:
    """Class for quaternion objects and operations on them.

    A quaternion is a hypercomplex number that generalizes the complex numbers.
    It can be represented as a 4-tuple (w, x, y, z) where w is the real part and
    x, y, and z are the imaginary parts. The imaginary parts are often
    represented as a vector (x, y, z).

    The class provides methods for creating quaternions from different
    representations, performing arithmetic operations, and converting between
    representations.

    Attributes:
        real: The real part of the quaternion.
        vector: The vectorial part of the quaternion as a numpy array.
    """

    def __init__(self, w: float, x: float, y: float, z: float) -> None:
        """Initializes a quaternion from its components.

        Args:
            w: The real part of the quaternion.
            x: The first imaginary part of the quaternion.
            y: The second imaginary part of the quaternion.
            z: The third imaginary part of the quaternion.
        """
        self.full = np.array([w, x, y, z])
        self.matrix = np.array([[w + 1j * x, y + 1j * z], [-y + 1j * z, w - 1j * x]])

    @property
    def real(self) -> float:
        """Returns the real part of the quaternion."""
        return self.full[0]

    @real.setter
    def real(self, value: float) -> None:
        """Sets the real part of the quaternion."""
        self.full[0] = value

    @property
    def vector(self) -> np.ndarray:
        """Returns the vectorial part of the quaternion."""
        return self.full[1:]

    @vector.setter
    def vector(self, value: np.ndarray) -> None:
        """Sets the vectorial part of the quaternion."""
        self.full[1:] = value

    def __mul__(self, other: Quaternion) -> Quaternion:
        """Multiplies two quaternions."""
        w = self.real * other.real - np.dot(self.vector, other.vector)
        v = (
            self.real * other.vector
            + other.real * self.vector
            + np.cross(self.vector, other.vector)
        )
        return Quaternion(w, *v)

    def __str__(self) -> str:
        """Returns a string representation of the quaternion."""
        return f"({self.real}, {self.vector[0]}, {self.vector[1]}, {self.vector[2]})"

    def __getitem__(self, index: int) -> float:
        """Returns the component of the quaternion at the given index."""
        return self.full[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Sets the component of the quaternion at the given index."""
        self.full[index] = value

    @classmethod
    def from_matrix(cls, matrix: np.ndarray) -> Quaternion:
        """Creates a quaternion from a unitary matrix.

        Args:
            matrix: The unitary matrix representation of the quaternion.

        Returns:
            The quaternion represented by the matrix.
        """
        w = matrix[0, 0].real
        x = matrix[0, 0].imag
        y = matrix[0, 1].real
        z = matrix[0, 1].imag
        return cls(w, x, y, z)

    def normalize(self) -> None:
        """Normalizes the quaternion."""
        norm: float = self.norm()
        self.real /= norm
        self.vector /= norm

    def normalized(self) -> Quaternion:
        """Returns a normalized copy of the quaternion."""
        norm: float = self.norm()
        return Quaternion(self.real / norm, *self.vector / norm)

    def conjugate(self) -> None:
        """Conjugates the quaternion."""
        self.vector *= -1

    def conjugated(self) -> Quaternion:
        """Returns a conjugated copy of the quaternion."""
        return Quaternion(self.real, *-self.vector)

    def norm(self) -> float:
        """Returns the norm of the quaternion."""
        return float(np.linalg.norm(self.full))

    def inverse(self) -> Quaternion:
        """Returns the inverse of the quaternion."""
        return Quaternion(
            self.real / self.norm() ** 2, *-self.vector / self.norm() ** 2
        )

    def to_unitary_matrix(self) -> np.ndarray:
        """Returns the unitary matrix representation of the quaternion."""
        w, x, y, z = self.full
        return np.array(
            [
                [w + x * 1j, y + z * 1j],
                [-y + z * 1j, w - x * 1j],
            ]
        )


def quaternion_from_angle_and_axis(theta: float, axis: np.ndarray) -> Quaternion:
    """Creates a quaternion from an angle and an axis of rotation.

    Args:
        theta: The angle of rotation in radians.
        axis: The axis of rotation as a 3D vector.

    Returns:
        The quaternion representing the rotation.
    """
    axis = axis / np.linalg.norm(axis)
    w = np.cos(theta / 2)
    v = np.sin(theta / 2) * axis
    return Quaternion(w, *v)
