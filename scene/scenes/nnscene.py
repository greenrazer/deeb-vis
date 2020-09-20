from scene.scenes.scene import Scene

from shaders.bufferbuilders.globalmtfbufferbuilder import GlobalMTFBufferBuilder

class NNScene(Scene):
    def __init__(self, camera, renderer): 
        self.curr_timing = 0
        self.steps = []
        self.activations = []
        Scene.__init__(self,
            camera = camera, 
            renderer = renderer)

    def add_mba_step_transformation(self, matrix, bias, activation, m_timing, b_timing, a_timing):
        m_time = (self.curr_timing + m_timing[0], self.curr_timing + m_timing[1])
        b_time = (m_time[1] + b_timing[0], m_time[1] + b_timing[1])
        a_time = (b_time[1] + a_timing[0], b_time[1] + a_timing[1])
        self.curr_timing = a_time[1]

        self.activations.append(activation)
        self.steps.append({
            'matrix': matrix, 
            'bias': bias, 
            'activation': activation, 
            'm_time': m_time, 
            'b_time': b_time, 
            'a_time': a_time
        })

    def add_transformations_to_uniforms(self):
        if not self.compiled:
            raise RuntimeError("Must compile shaders before attaching transformations to uniforms")
        for c in self.buffer_builders:
            if isinstance(c, GlobalMTFBufferBuilder):
                for i in range(len(self.steps)):
                    c.set_step_uniform(i, 
                        self.steps[i]['matrix'].to_tuple(), 
                        self.steps[i]['bias'].to_tuple(),
                        self.steps[i]['m_time'],
                        self.steps[i]['b_time'],
                        self.steps[i]['a_time']
                    )

    def compile(self):
        Scene.compile(self)
        self.add_transformations_to_uniforms()

    def generate_buffer_builders(self):
        buffer_builders = []
        for clas in self.buffer_builder_classes:
            buf_cls = clas(self.scene_objs, self.activations)
            if buf_cls.populated:
                buffer_builders.append(buf_cls)
        return buffer_builders
