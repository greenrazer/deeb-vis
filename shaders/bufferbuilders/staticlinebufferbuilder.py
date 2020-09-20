from scene.objects.line import Line
from scene.objects.grid import Grid

from shaders.bufferbuilders.bufferbuilder import BufferBuilder

from shaders.programbuilders.staticlinebuilder import StaticLineBuilder

class StaticLineBufferBuilder(BufferBuilder):
    object_cls = Line
    acceptable_classes = (
        object_cls,
        Grid
    )

    def __init__(self, object_list, *args):
        BufferBuilder.__init__(self, object_list)

    def get_program_builder(self):
        return StaticLineBuilder()

    def is_correct_class(self, instance):
        return isinstance(instance, self.acceptable_classes) and not instance.animated