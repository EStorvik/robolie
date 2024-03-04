"""Module for the special orthogonal group in two and three dimensions."""

import numpy as np


class SO:
    """Special orthogonal group in two and three dimensions.

    This class provides methods for the special orthogonal group in two and
    three dimensions. The special orthogonal group is the group of all
    orthogonal matrices with determinant 1. The group is denoted by SO(n),
    where n is the dimension of the space.

    Attributes:
        angle (float): The angle of rotation.
        axis (numpy.ndarray): The axis of rotation.
    """

    def __init__(self, angle, axis):
        """Initialize the SO class.

        Args:
            **kwargs: keyword arguments.
        """
        self.angle = angle
        self.axis = axis
        self.matrix = self._compute_matrix()

    def _compute_matrix(self):
        """Compute the rotation matrix.

        Returns:
            numpy.ndarray: The rotation matrix.
        """
        return np.array([[np.cos(self.angle) + self.axis[0] ** 2 * (1 - np.cos(self.angle)),
                          self.axis[0] * self.axis[1] * (1 - np.cos(self.angle)) - self.axis[2] * np.sin(self.angle),
                          self.axis[0] * self.axis[2] * (1 - np.cos(self.angle)) + self.axis[1] * np.sin(self.angle)],
                         [self.axis[1] * self.axis[0] * (1 - np.cos(self.angle)) + self.axis[2] * np.sin(self.angle),
                          np.cos(self.angle) + self.axis[1] ** 2 * (1 - np.cos(self.angle)),
                          self.axis[1] * self.axis[2] * (1 - np.cos(self.angle)) - self.axis[0] * np.sin(self.angle)],
                         [self.axis[2] * self.axis[0] * (1 - np.cos(self.angle)) - self.axis[1] * np.sin(self.angle),
                          self.axis[2] * self.axis[1] * (1 - np.cos(self.angle)) + self.axis[0] * np.sin(self.angle),
                          np.cos(self.angle) + self.axis[2] ** 2 * (1 - np.cos(self.angle))]])
    def __str__(self):
        return "Special orthogonal group in two and three dimensions"

    def __repr__(self):
        return "SO()"

    def __eq__(self, other):
        return isinstance(other, SO)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(SO)

    def __copy__(self):
        return SO()

    def __deepcopy__(self, memo):
        return SO()