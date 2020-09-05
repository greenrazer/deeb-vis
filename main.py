from renderer import Renderer
from lineR import LineR
from vector3 import Vector3
from line_utils import circle_pts, random_pts, straight_line_pts, create_grid

import math
import random


grid = create_grid(-5, 5, 1, 1)

buf = bytes()
for line in grid:
    buf += line.to_bytes()

render = Renderer(buf)
def b4_frame(render_window, timer):
    render_window.prog['eye'].value = (5*math.cos(timer*0.1), 5*math.sin(timer*0.1), 3)

render.run(before_frame_func=b4_frame)