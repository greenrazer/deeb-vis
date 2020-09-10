import math
import time as tim

from base.matrix3 import Matrix3
from base.vector3 import Vector3
from renderable.grid import Grid
from renderable.sphere import Sphere
from renderable.spheregrid import SphereGrid
from renderer.renderer import Renderer

from base.sphere3 import Sphere3

grid = Grid(-5, 5)
grid_bytes = grid.to_bytes()

spheres = SphereGrid(-2, 2, 0.5, sections=1)

rm = Matrix3.random(-1, 1)

def trans(location):
    return rm @ location

# def trans2(sph,i):
#     sph[i].location = rm @ sph[i].location

# spheres.in_place_transform(trans2)
spheres.animate_transform(trans, 15.0)

def b4_frame(render_window, time, frame_time):
    # render_window.prog['eye'].value = (5*math.cos(time*0.1), 5*math.sin(time*0.1), 5)
    pass

render = Renderer(grid_bytes + spheres.to_bytes())
# render.run( change_vertex_buffer=change_verex_arr, before_frame_func=b4_frame)
render.run( before_frame_func=b4_frame)