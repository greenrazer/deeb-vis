import math

from base.matrix3 import Matrix3
from base.vector3 import Vector3
from base.vector import Vector
from base.matrix import Matrix

from scene.objects.grid import Grid
from scene.objects.spheregrid import SphereGrid
from scene.objects.linegrid import LineGrid
from scene.objects.sphere import Sphere
from scene.objects.spherecollection import SphereCollection
from scene.objects.vector import Vector as VectorR

from scene.cameras.perspectivecamera import PerspectiveCamera
from scene.cameras.orthographiccamera import OrthographicCamera

from scene.scenes.nnscene import NNScene

from renderer.windowrenderer import WindowRenderer

from datagenerators.nntrainer import NNTrainer


SIGMOID_FUNC = "1.0/(1.0 + exp(-a))"
SOFTMAX_FUNC = "exp(a)/(exp(a.x)+exp(a.y)+exp(a.z))"

class NNSceneManager:
    def __init__(self, data, layers, labels):
        if len(data) != len(labels):
            raise RuntimeError("labels and data dont match")

        self.renderer = WindowRenderer()

        self.ang = 0
        self.camera_perspective = PerspectiveCamera(Vector3(0.0, 5.0, 5.0), 0.1, 1000, 1, math.pi/3)
        self.camera_perspective.look_at(Vector3(0.0,0.0,0.0), Vector3(0.0,0.0,1.0))

        self.z = 20
        self.camera_orthographic = OrthographicCamera(Vector3(0.0, 0.0, 100.0), self.z, self.z, -self.z, -self.z, 0.1, 1000)
        self.camera_orthographic.look_at(Vector3(0.0,0.0,0.0), Vector3(1.0,0.0,0.0))

        self.scene = NNScene(self.camera_perspective, self.renderer)
        self.scene.renderer.add_before_render_function(self.rotate)

        # self.scene = NNScene(self.camera_orthographic, self.renderer)
        # self.scene.renderer.add_before_render_function(self.zoom)

        self.neural_network = NNTrainer(data, layers, labels)
        self.neural_network.n_training_epochs(10000)

        self.setup(data, labels)

    def setup(self, data, labels):
        self.spheres = SphereGrid(-2, 2, 1, radius = 0.03)
        self.lines = LineGrid(-20,20, grid_increment=2)
        self.grid = Grid(-20, 20, grid_width=0.0008)
        self.vector = VectorR.straight_vector(Vector3(0,0,0.01), Vector3(4,4,0.01), 0.5, 0.026)

        self.datas = SphereCollection(0.003)
        for d in range(len(data)):
            self.datas.add(
                Vector(*data[d]).pad_to(3),
                Vector(*labels[d]).pad_to(3),
            )

        self.scene.add_static_object(self.grid)
        self.scene.add_transformable_object(self.vector)
        self.scene.add_transformable_object(self.spheres)
        self.scene.add_transformable_object(self.lines)
        # self.scene.add_transformable_object(self.datas)

        for l in self.neural_network.layers_history[-1]:
            mat = Matrix.from_array(l['weights']).pad_to(3)
            trans = Vector.from_array(l['bias']).pad_to(3)
            self.scene.add_mba_step_transformation(mat, trans, SIGMOID_FUNC, (0,5), (0,5), (0,5))

    def zoom(self, renderer, time, frametime):
        if abs(frametime) > 1500000:
            return
        if 2 < time and self.z > 2:
            self.camera_orthographic.update(self.z, self.z, -self.z, -self.z, 0.1, 1000)
            if self.camera_orthographic.position.z > 1:
                self.camera_orthographic.position -= Vector3(0.0, 0.0, 5*frametime)
            self.z -= frametime

    def rotate(self, renderer, time, frametime):
        if abs(frametime) > 1500000:
            return
        self.camera_perspective.position = Vector3(10*math.cos(self.ang), 10*math.sin(self.ang), 5)
        self.ang += frametime*0.02

    def play(self):
        self.scene.compile()
        self.scene.run()