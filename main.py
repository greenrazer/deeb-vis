from renderer import Renderer
from lineR import LineR
from vector3 import Vector3
from sphereR import SphereR
from gridR import GridR
from lineutils import circle_pts, random_pts

import math
import random


grid = GridR(-5, 5)
grid_bytes = grid.to_bytes()

point1 = SphereR(0.2, Vector3(1, 0, 0), (1.0, 1.0, 0.0))
point2 = SphereR(0.2, Vector3(2, 0, 0), (1.0, 1.0, 0.0))
point3 = SphereR(0.2, Vector3(3, 0, 0), (1.0, 1.0, 0.0))

def change_verex_arr(render_window, time, frame_time):
    point1.location = Vector3(1*math.cos(time*0.3), 1*math.sin(time*0.3),0)
    point2.location = Vector3(2*math.cos(time*0.6), 0, 2*math.sin(time*0.6))
    point3.location = Vector3(0,3*math.cos(time*0.9), 3*math.sin(time*0.9))
    buf = grid_bytes + point1.to_bytes() + point2.to_bytes() + point3.to_bytes()
    return buf

def b4_frame(render_window, time, frame_time):
    render_window.prog['eye'].value = (5*math.cos(time*0.1), 5*math.sin(time*0.1), 5)

render = Renderer()
render.run(change_vertex_buffer=change_verex_arr, before_frame_func=b4_frame)