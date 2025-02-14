from shaders.programbuilders.programbuilder import ProgramBuilder
from shaders.programbuilders.functionbuilder import create_glsl_function

from utils.util import replace_with_all



class GlobalMTFBuilder(ProgramBuilder):
    def __init__(self, activation_list):
        ProgramBuilder.__init__(self)

        with open("shaders/scripts/vert_successive_tween_begin.frag.glsl") as f:
            self.begin_tween_step_template = f.read()

        with open("shaders/scripts/vert_successive_tween_step.frag.glsl") as f:
            self.middle_tween_step_template = f.read()

        self.activation_list = activation_list
        self.activation_function_name_stub = lambda x : f'activation_function_{x}'

        self.uniforms_token = '<uniforms>'
        self.activation_functions_token = '<activations>'
        self.start_token = '<start_pt>'
        self.matrix_token = '<matrix>'
        self.bias_token = '<bias>'
        self.activation_token = '<activation>'

        self.matrix_time_start_token = '<matrix_time_start>'
        self.matrix_time_end_token = '<matrix_time_end>'
        self.bias_time_start_token = '<bias_time_start>'
        self.bias_time_end_token = '<bias_time_end>'
        self.activation_time_start_token = '<activation_time_start>'
        self.activation_time_end_token = '<activation_time_end>'

        self.main_step_sphere_replace_token = '<matrix_step_sphere_transform>'
        self.main_step_line_before_vertex_replace_token = '<b4_vert_matrix_transform>'
        self.main_step_line_curr_vertex_replace_token = '<curr_vert_matrix_transform>'
        self.main_step_line_after_vertex_replace_token = '<after_vert_matrix_transform>'

        self.matrix_prefix = 'change_matrix_'
        self.bias_prefix = 'change_bias_'
        self.matrix_time_prefix = 'matrix_change_start_stop_time_'
        self.bias_time_prefix = 'bias_change_start_stop_time_'
        self.activation_time_prefix = 'activation_change_start_stop_time_'

        self.uniforms = [
            "projection_matrix", 
            "camera_pos",
            "time",
        ]
        self.step_uniforms = []

    def generate_activations(self):
        self.step_to_function_name = []

        expressions = []
        for s in self.activation_list:
            if s not in expressions:
                expressions.append(s)
                ind = len(expressions)-1
            else:
                ind = expressions.index(s)
            self.step_to_function_name.append(self.activation_function_name_stub(ind))

        activations_functions = []
        for ind, func in enumerate(expressions):
            glsl_function = create_glsl_function(self.activation_function_name_stub(ind), 'vec3', func)
            activations_functions.append(glsl_function)
        
        return "\n".join(activations_functions)

    def generate_uniforms(self):
        self.step_uniforms = []
        uniforms_arr = []
        for i in range(len(self.activation_list)):
            uniforms = (
                f'{self.matrix_prefix}{i}',
                f'{self.bias_prefix}{i}',
                f'{self.matrix_time_prefix}{i}',
                f'{self.bias_time_prefix}{i}',
                f'{self.activation_time_prefix}{i}',
            )

            uniforms_arr_str = [
                f'uniform mat3 {uniforms[0]};\n',
                f'uniform vec3 {uniforms[1]};\n',
                f'uniform vec2 {uniforms[2]};\n',
                f'uniform vec2 {uniforms[3]};\n',
                f'uniform vec2 {uniforms[4]};\n'
            ]

            self.uniforms.extend(uniforms)
            self.step_uniforms.append(uniforms)
            uniforms_arr.append("".join(uniforms_arr_str))
        return "".join(uniforms_arr)

    def generate_step_transformation_fragments(self, init_vec):
        function_template_list = []
        for i, step in enumerate(self.activation_list):
            if(i == 0):
                temp = self.begin_tween_step_template.replace(self.matrix_token, f'{self.matrix_prefix}{i}')
                temp = temp.replace(self.start_token, init_vec)
            else:
                temp = self.middle_tween_step_template.replace(self.matrix_token, f'{self.matrix_prefix}{i}')
            
            temp = temp.replace(self.bias_token, f'{self.bias_prefix}{i}')
            temp = temp.replace(self.activation_token, f'{self.step_to_function_name[i]}')

            temp = temp.replace(self.matrix_time_start_token, f'{self.matrix_time_prefix}{i}.x')
            temp = temp.replace(self.matrix_time_end_token, f'{self.matrix_time_prefix}{i}.y')
            temp = temp.replace(self.bias_time_start_token, f'{self.bias_time_prefix}{i}.x')
            temp = temp.replace(self.bias_time_end_token, f'{self.bias_time_prefix}{i}.y')
            temp = temp.replace(self.activation_time_start_token, f'{self.activation_time_prefix}{i}.x')
            temp = temp.replace(self.activation_time_end_token, f'{self.activation_time_prefix}{i}.y')
            
            function_template_list.append(temp)
        
        if(len(self.activation_list) == 0):
            function_template_list.append(f"tween_val = 0.0; before = {init_vec};after = vec3(0.0,0.0,0.0);\n")

        return "".join(function_template_list)

    def build_vertex_shader(self):
        activation_functions_string = self.generate_activations()
        steps_uniform_string = self.generate_uniforms()
        step_fragments_string = self.generate_step_transformation_fragments('<start_pt>')

        step_sphere_fragments_string = step_fragments_string.replace('<start_pt>', 'translate_from')
        step_list_fragments_string = step_fragments_string.replace('<start_pt>', 'from_vert')

        step_line_before_fragments_string = step_fragments_string.replace('<start_pt>', 'before_vert')
        step_line_curr_fragments_string = step_fragments_string.replace('<start_pt>', 'from_vert')
        step_line_after_fragments_string = step_fragments_string.replace('<start_pt>', 'after_vert')

        final_shader = replace_with_all(self.vertex_shader_template, [
            (self.main_step_sphere_replace_token, step_sphere_fragments_string),
            (self.uniforms_token, steps_uniform_string),
            (self.main_step_list_replace_token, step_list_fragments_string),
            (self.main_step_line_before_vertex_replace_token, step_line_before_fragments_string),
            (self.main_step_line_curr_vertex_replace_token, step_line_curr_fragments_string),
            (self.main_step_line_after_vertex_replace_token, step_line_after_fragments_string),
            (self.activation_functions_token, activation_functions_string)
        ])

        with open('shaders/temp_vert_shader_out_DEBUG.glsl', 'w') as f:
            f.write(final_shader)

        return final_shader
