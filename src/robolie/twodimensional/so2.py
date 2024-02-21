""" Rotations in two spatial dimensions. Including exponential
and logarithmic maps to and from the lie algebra of the unit
circle/two-dimensional rotation group. """

from __future__ import annotations

import numpy as np


class SO2:
    """Class for 2D rotations."""

    def __init__(self, angle: float) -> None:
        """Initializes a 2D rotation.

        Args:
            angle: The angle of rotation in radians.
        """
        self.angle = angle

    def __mul__(self, other: SO2) -> SO2:
        """Multiplies two 2D rotations."""
        return SO2(self.angle + other.angle)

    @property
    def matrix(self) -> np.ndarray:
        return np.array(
            [
                [np.cos(self.angle), -np.sin(self.angle)],
                [np.sin(self.angle), np.cos(self.angle)],
            ]
        )

    @property
    def complex(self) -> complex:
        return np.exp(1j * self.angle)

    @classmethod
    def exp(cls, omega: float) -> SO2:
        """Exponential map to the lie group of 2D rotations.

        Args:
            omega: The element of the lie algebra to map.

        Returns:
            The corresponding element of the lie group.
        """
        return cls(omega)

    def log(self) -> float:
        """Logarithmic map to the lie algebra of 2D rotations.

        Args:
            other: The element of the lie group to map.

        Returns:
            The corresponding element of the lie algebra.
        """
        return self.angle

    def __str__(self) -> str:
        return f"SO2({self.angle})"
