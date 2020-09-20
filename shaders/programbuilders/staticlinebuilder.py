from shaders.programbuilders.programbuilder import ProgramBuilder

class StaticLineBuilder(ProgramBuilder):
    def __init__(self):
        ProgramBuilder.__init__(self)

        with open("shaders/scripts/static_line_vert_shader.frag.glsl") as f:
            self.vertex_shader_template = f.read()

        with open("shaders/scripts/color_fragment_shader.frag.glsl") as f:
            self.fragment_shader_template = f.read()

        self.input_tuple_per_vertex = self.generate_input_tuple(
            [
                ('3f4', 'before_vert'),
                ('3f4', 'curr_vert'),
                ('3f4', 'after_vert'),
                ('1f4', 'width'),
                ('3f4', 'in_color'),
                ('1u1', 'type'),
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
            "projection_matrix", 
            "camera_pos"
        ]

    def build_vertex_shader(self):
        with open('shaders/static_line_vert_shader_out_DEBUG.glsl', 'w') as f:
            f.write(self.vertex_shader_template)

        return self.vertex_shader_template
    
    def build_fragment_shader(self):
        return self.fragment_shader_template
