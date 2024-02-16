import robolie as rl

import numpy as np

def test_quaternion_initialization():
    q = rl.Quaternion(1, 2, 3, 4)
    assert q.real == 1
    assert np.array_equal(q.vector, np.array([2, 3, 4]))