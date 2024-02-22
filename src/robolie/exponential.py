"""Geberal exponential function for various Lie algebras"""

import robolie as rl


def exp(x):
    """Returns the exponential of x. Function changes depending on the type of x."""
    if type(x) == rl.PureQuaternion:
        return x.exp()
    else:
        raise NotImplementedError(f"Exponential not implemented for {type(x)}")
