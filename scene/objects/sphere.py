from base.sphere3 import Sphere3
from base.vector3 import Vector3
from scene.objects.transformablesceneobject import TransformableSceneObject

class Sphere(Sphere3, TransformableSceneObject):
    def __init__(self, radius, location, color = None, subdivisions = 2):
        Sphere3.__init__(self, radius, location, subdivisions)
        TransformableSceneObject.__init__(self)

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
        self.animated = True
        self.animated_location = Vector3(0.0,0.0,0.0)
        self.animated_time = 0.0

    def animate_to(self, location, time):
        self.animated = True
        self.animated_location = location
        self.animated_time = time
        

    @property
    def shader_info(self):
        shader_data = []
        for triangle in self.triangles:
            color = self.color_array[self.c] if self.color is None else self.color
            for vert in triangle:
                shader_data.extend(
                    [vert[0],vert[1],vert[2], 0.0,0.0,0.0, self.location[0],self.location[1],self.location[2], self.animated_location[0],self.animated_location[1],self.animated_location[2], 0.0,self.animated_time, 0.0,0.0,0.0,  0.0,0.0,1.0,  self.radius, color[0],color[1],color[2],  4 if self.animated else 1],
                )
            self.c = (self.c + 1) % 6
        return shader_data

