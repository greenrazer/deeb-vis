from sphere3 import Sphere3
from renderable import Renderable

class SphereR(Sphere3, Renderable):
    def __init__(self, radius, location, color = None, subdivisions = 2):
        Sphere3.__init__(self, radius, location, subdivisions)
        Renderable.__init__(self)

        self.color = color

        self.color_array = [
            [1.0,0.0,0.0],
            [0.0,1.0,0.0],
            [0.0,0.0,1.0],
            [1.0,1.0,0.0],
            [0.0,1.0,1.0],
            [1.0,0.0,1.0],
        ]
        self.c = 0

    @property
    def shader_info(self):
        shader_data = []
        for triangle in self.triangles:
            color = self.color_array[self.c] if self.color is None else self.color
            for vert in triangle:
                shader_data.append(
                    [vert[0],vert[1],vert[2],  self.location[0],self.location[1],self.location[2],  0.0,0.0,0.0,  0.0,0.0,1.0,  self.radius, color[0],color[1],color[2],  1],
                )
            self.c = (self.c + 1) % 6
        return shader_data

