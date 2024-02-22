"""General implementation of the logarithmic function"""

import robolie as rl


def log(x):
    """Returns the logarithm of x. Function changes
    depending on the type of x."""
    if isinstance(x, rl.Quaternion):
        return x.log()
    else:
        raise NotImplementedError(f"Logarithm not implemented for {type(x)}")
