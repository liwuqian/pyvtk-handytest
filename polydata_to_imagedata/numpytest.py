import numpy as np
p1 = np.array([-1, 0, 0])
p2 = np.array([0, -1, 0])
p3 = np.cross(p1, p2)
print(p3)