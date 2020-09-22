from shaders.programbuilders.programbuilder import ProgramBuilder

class ScreenBuilder(ProgramBuilder):
    def __init__(self):
        ProgramBuilder.__init__(self)

        with open("shaders/scripts/screen_vert_shader.frag.glsl") as f:
            self.vertex_shader_template = f.read()

        with open("shaders/scripts/screen_fragment_shader.frag.glsl") as f:
            self.fragment_shader_template = f.read()

        self.input_tuple_per_vertex = self.generate_input_tuple(
            [
                ('3f4', 'vert'),
                ('2f4', 'texture_coord')
            ],
            self.PER_VERTEX
        )

        self.input_tuple_per_instance = self.generate_input_tuple(
            [],
            self.PER_INSTANCE
        )

        self.input_tuple_per_render = self.generate_input_tuple(
            [],
            self.PER_RENDER
        )

        self.uniforms = [
            "projection_matrix"
        ]

    def build_vertex_shader(self):
        return self.vertex_shader_template
    
    def build_fragment_shader(self):
        return self.fragment_shader_template
