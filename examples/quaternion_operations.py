import robolie as rl

import numpy as np

# Create a quaternion
q1 = rl.Quaternion(1, 2, 3, 4)
q2 = rl.Quaternion(5, 6, 7, 8)

print(rl.rotate_by_quaternion(np.array([1,1,0]), np.pi, np.array([1, 0, 0])))