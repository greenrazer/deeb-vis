from scene.objects.transformablesceneobject import TransformableSceneObject
from scene.objects.sphere import Sphere

class SphereCollection(TransformableSceneObject):
    def __init__(self, radius = 0.1):
        TransformableSceneObject.__init__(self)
        self.spheres = []
        self.radius = radius
    
    def add(self, loc, color):
        self.spheres.append(
            Sphere(
                self.radius, 
                loc, 
                color
            )
        )
    
    @property
    def num_verts(self):
        verts = 0
        for s in self.spheres:
            verts += s.num_verts
        return verts


    @property
    def shader_info(self):
        shader_data = []
        for sphere in self.spheres:
            vals = sphere.shader_info
            shader_data.extend(vals)
        return shader_data