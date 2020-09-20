from scene.objects.line import Line
from scene.objects.linegrid import LineGrid

from shaders.bufferbuilders.globalmtfbufferbuilder import GlobalMTFBufferBuilder

from shaders.programbuilders.translinebuilder import TransLineBuilder

class TransLineBufferBuilder(GlobalMTFBufferBuilder):
    object_cls = Line
    acceptable_classes = (
        object_cls,
        LineGrid
    )

    def get_program_builder(self):
        return TransLineBuilder(self.activations)

    def is_correct_class(self, instance):
        return isinstance(instance, self.acceptable_classes) and instance.animated