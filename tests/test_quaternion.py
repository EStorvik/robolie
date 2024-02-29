import robolie as rl

import numpy as np

def test_quaternion_initialization():
    q = rl.Quaternion(1, 2, 3, 4)
    assert q.real == 1
    assert np.array_equal(q.vector, np.array([2, 3, 4]))


def test_quaternion_multiplication():
    q1 = rl.Quaternion(1, 2, 3, 4)
    q2 = rl.Quaternion(5, 6, 7, 8)
    q3 = q1 * q2
    assert q3.real == -60
    assert np.array_equal(q3.vector, np.array([12, 30, 24]))

    matrix = q1.matrix @ q2.matrix
    q4 = rl.Quaternion.from_matrix(matrix)
    assert np.allclose(q3.vector, q4.vector)
    assert np.isclose(q3.real, q4.real)

def test_quaternion_averaging():
    rotations = [
        (np.pi / 4, np.array([0, 1, 0])),
        (np.pi / 3, np.array([0, 1/np.sqrt(2), 1/np.sqrt(2)])),
        (np.pi / 2, np.array([0, 0, 1])),
    ]

    avg_quaternion = rl.compute_average_rotation_quaternion(rotations)
    avg_angle, avg_axis = avg_quaternion.which_rotation()
    assert np.isclose(avg_angle, 0.9553166181245093)
    assert np.allclose(avg_axis, np.array([0.0, 0.7071067811865475, 0.7071067811865475]))