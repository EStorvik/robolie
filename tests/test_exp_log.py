import robolie as rl

import numpy as np

def test_exp_log():
    q = rl.Quaternion(-1, 2, -3, 4)
    q.normalize()
    log_q = rl.log(q)
    z = log_q
    assert type(log_q) == rl.PureQuaternion
    assert np.allclose(q.full,rl.exp(log_q).full)
    assert np.allclose(z.vector, rl.log(rl.exp(z)).vector)
