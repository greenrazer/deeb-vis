from scene.objects.screen import Screen

from shaders.bufferbuilders.bufferbuilder import BufferBuilder

from shaders.programbuilders.screenbuilder import ScreenBuilder

class ScreenBufferBuilder(BufferBuilder):
    object_cls = Screen
    acceptable_classes = (
        object_cls
    )

    def __init__(self, object_list, *args):
        BufferBuilder.__init__(self, object_list)

    def get_program_builder(self):
        return ScreenBuilder()

    def is_correct_class(self, instance):
        return isinstance(instance, self.acceptable_classes)