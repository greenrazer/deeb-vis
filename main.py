import math

from base.matrix3 import Matrix3
from base.vector3 import Vector3

from scene.objects.grid import Grid
from scene.objects.spheregrid import SphereGrid

from scene.cameras.perspectivecamera import PerspectiveCamera
from scene.cameras.orthographiccamera import OrthographicCamera

from scene.scenes.nnscene import NNScene

from renderer.windowrenderer import WindowRenderer

MINIMUM_FLOAT = 1.18e-38


grid = Grid(-5, 5)
spheres = SphereGrid(-2, 2, 0.5, sections=1)

# camera = PerspectiveCamera(Vector3(0.0, 5.0, 5.0), 0.1, 1000, 1, math.pi/3)
camera = OrthographicCamera(Vector3(0.0, 0.0, 5.0), 5, 5, -5, -5, 0.1, 1000)
camera.look_at(Vector3(0.0,0.0,0.0), Vector3(1.0,0.0,0.0))

# def zoom(renderer, time, frametime):
#     if(abs(frametime) > 1500000000):
#         return
#     update = -1*frametime
#     camera.position = camera.position + Vector3(0.0,0.0,update)

amnt = 0
def zoom(renderer, time, frametime):
    if(abs(frametime) > 1500000000):
        return
    global amnt
    update = 0.1*frametime/2
    amnt += update
    camera.update(5 - amnt, 5 - amnt, -5 + amnt, -5 + amnt, 0.1, 1000)

renderer = WindowRenderer()
renderer.add_before_render_function(zoom)

scene = NNScene(camera, renderer)
scene.add_static_object(grid)
scene.add_transformable_object(spheres)

scene.add_mba_step_transformation(Matrix3.random(-1,1), Vector3.random(-1,1), "1.0/(1.0 + exp(-a))", (0,5), (0,5), (0,5))
scene.add_mba_step_transformation(Matrix3.random(-1,1), Vector3.random(-1,1), "1.0/(1.0 + exp(-a))", (0,5), (0,5), (0,5))
scene.add_mba_step_transformation(Matrix3.random(-1,1), Vector3.random(-1,1), "1.0/(1.0 + exp(-a))", (0,5), (0,5), (0,5))

scene.compile()
scene.run()