import numpy as np

import robolie as rl

rot1 = rl.SO2(np.pi / 4)
rot2 = rl.SO2(np.pi / 12)
rot3 = rot1 * rot2
rot4 = rl.SO2(1.5)


avg_rotation = rl.SO2.exp((rot1.log() + rot2.log() + rot3.log() + rot4.log())/4)


print(avg_rotation)

print(avg_rotation.matrix)