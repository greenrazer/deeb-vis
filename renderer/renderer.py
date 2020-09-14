class Renderer:
    def __init__(self):
        self.before_render_funcs = []
        self.after_render_funcs = []

    def set_program(self, program):
        self.program = program

    def add_before_render_function(self, func):
        self.before_render_funcs.append(func)

    def add_after_render_function(self, func):
        self.after_render_funcs.append(func)

    def update_vertex_buffer(self, buffer):
        self.vbo.write(buffer)

    def set_vertex_buffer(self, byte_array):
        self.shader_args = ("3f4 3f4 3f4 3f4 2f4 3f4 3f4 1f4 3f4 u1 /v", 
            "from_vert", 
            "to_vert", 
            "translate_from", 
            "translate_to", 
            "point_transform_start_stop_time", 
            "normal", 
            "light_direction", 
            "width_scale", 
            "in_color", 
            "type")

        self.vbo = self.context.buffer(byte_array)
        self.vao = self.context.vertex_array(self.program, [
            (self.vbo, *self.shader_args),
        ])

    def run(self):
        raise NotImplementedError("A subclass of renderer must be instansiated")