from shaders.programbuilders.globalmtfbuilder import GlobalMTFBuilder

from utils.util import replace_with_all

class TransSphereBuilder(GlobalMTFBuilder):
    def __init__(self, activation_functions):
        GlobalMTFBuilder.__init__(self, activation_functions)

        with open("shaders/scripts/trans_sphere_vert_shader.frag.glsl") as f:
            self.vertex_shader_template = f.read()

        with open("shaders/scripts/color_fragment_shader.frag.glsl") as f:
            self.fragment_shader_template = f.read()

        self.input_tuple_per_vertex = self.generate_input_tuple(
            [
                ('3f4', 'curr_vert'),
                ('3f4', 'translate'),
                ('1f4', 'scale'),
                ('3f4', 'in_color'),
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
            "camera_pos",
            "time",
            "light_direction"
        ]

    def build_vertex_shader(self):
        activation_functions_string = self.generate_activations()
        steps_uniform_string = self.generate_uniforms()
        step_fragments_string = self.generate_step_transformation_fragments('<start_pt>')

        step_sphere_fragments_string = step_fragments_string.replace('<start_pt>', 'translate')

        final_shader = replace_with_all(self.vertex_shader_template, [
            (self.uniforms_token, steps_uniform_string),
            (self.main_step_sphere_replace_token, step_sphere_fragments_string),
            (self.activation_functions_token, activation_functions_string)
        ])

        with open('shaders/trans_sphere_vert_shader_out_DEBUG.glsl', 'w') as f:
            f.write(final_shader)

        return final_shader

    def build_fragment_shader(self):
        return self.fragment_shader_template
