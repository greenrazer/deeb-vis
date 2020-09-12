from vector3 import Vector3
from lineR import LineR

import math
import random

def circle_pts(sections, radius):
    theta = (2*math.pi)/sections
    out = []
    for num in range(sections):
        out.append(Vector3(radius*math.cos(theta*num), radius*math.sin(theta*num), 0.0))
    out.append(out[0])
    return out

def random_pts(sections):
    out = []
    for num in range(sections):
        out.append(Vector3(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))
    return out
