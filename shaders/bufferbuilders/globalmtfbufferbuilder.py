from shaders.bufferbuilders.bufferbuilder import BufferBuilder

class GlobalMTFBufferBuilder(BufferBuilder):
    acceptable_classes = ()

    def __init__(self, object_list, activations, *args):
        self.activations = activations
        BufferBuilder.__init__(self, object_list)

    def set_step_uniform(self, step, matrix, transform, matrix_time, transform_time, function_time):
        self.set_uniform(self.program_builder.step_uniforms[step][0], matrix)
        self.set_uniform(self.program_builder.step_uniforms[step][1], transform)
        self.set_uniform(self.program_builder.step_uniforms[step][2], matrix_time)
        self.set_uniform(self.program_builder.step_uniforms[step][3], transform_time)
        self.set_uniform(self.program_builder.step_uniforms[step][4], function_time)