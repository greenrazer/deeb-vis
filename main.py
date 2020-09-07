import math
import time as tim

from base.vector3 import Vector3
from renderable.grid import Grid
from renderable.sphere import Sphere
from renderable.spheregrid import SphereGrid
from renderer.renderer import Renderer

from base.sphere3 import Sphere3

grid = Grid(-5, 5)
grid_bytes = grid.to_bytes()

spheres = SphereGrid(-2, 2, 0.5, sections=1)

def change_verex_arr(render_window, time, frame_time):
    def trans(spheres, index):
        if spheres[index].location.z < math.hypot(*spheres[index].location.xy):
            spheres[index].location.z += math.hypot(*spheres[index].location.xy)*0.01
    
    spheres.in_place_transform(trans)
    return grid_bytes + spheres.to_bytes()

def b4_frame(render_window, time, frame_time):
    render_window.prog['eye'].value = (5*math.cos(time*0.1), 5*math.sin(time*0.1), 5)

render = Renderer(grid_bytes + spheres.to_bytes())
render.run( change_vertex_buffer=change_verex_arr, before_frame_func=b4_frame)
# render.run( before_frame_func=b4_frame)