from shaders.bufferbuilders.globalmtfbufferbuilder import GlobalMTFBufferBuilder

from shaders.programbuilders.transspherebuilder import TransSphereBuilder

from scene.objects.sphere import Sphere
from scene.objects.spherecollection import SphereCollection
from scene.objects.spheregrid import SphereGrid

class SphereBufferBuilder(GlobalMTFBufferBuilder):
    object_cls = Sphere
    acceptable_classes = (
        object_cls,
        SphereCollection,
        SphereGrid
    )

    def get_program_builder(self):
        return TransSphereBuilder(self.activations)

    def is_correct_class(self, instance):
        return isinstance(instance, self.acceptable_classes) and instance.animated