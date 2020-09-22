from base.vector3 import Vector3
from scene.objects.transformablesceneobject import TransformableSceneObject

class Screen(TransformableSceneObject):
    floats_per_vertex = 5
    chars_per_vertex = 0
    bytes_per_vertex = floats_per_vertex*4 + chars_per_vertex*1

    def __init__(self, a, b, c, d):
        TransformableSceneObject.__init__(self)
        self.corners = [a, b, c, d]

    @property
    def num_verts(self):
        return 6

    @property
    def shader_info(self):
        shader_data = [
            self.corners[0][0], self.corners[0][1], self.corners[0][2], 0.0, 1.0,
            self.corners[1][0], self.corners[1][1], self.corners[1][2], 1.0, 1.0,
            self.corners[2][0], self.corners[2][1], self.corners[2][2], 0.0, 0.0,

            self.corners[2][0], self.corners[2][1], self.corners[2][2], 0.0, 0.0,
            self.corners[1][0], self.corners[1][1], self.corners[1][2], 1.0, 1.0,
            self.corners[3][0], self.corners[3][1], self.corners[3][2], 1.0, 0.0,
        ]
        return shader_data

    @staticmethod
    def flat(self, location, width, height):
        w = width/2
        h = height/2
        return Screen(
            Vector3(location[0] - width, 0.0, location[0] + height),
            Vector3(location[0] + width, 0.0, location[0] + height),
            Vector3(location[0] - width, 0.0, location[0] - height),
            Vector3(location[0] + width, 0.0, location[0] - height)
        )

