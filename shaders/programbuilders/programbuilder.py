class ProgramBuilder:
    PER_VERTEX = '/v'
    PER_INSTANCE = '/i'
    PER_RENDER = '/r'
    def __init__(self):
        self.input_tuple_per_vertex = None
        self.input_tuple_per_instance = None
        self.input_tuple_per_render = None
        self.uniforms = []

    def build(self, context):
        vertex_shader = self.build_vertex_shader()
        fragment_shader = self.build_fragment_shader()
        return context.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )


    def build_vertex_shader(self):
        raise NotImplementedError("Vertex shader builder not implemented.")
    
    def build_fragment_shader(self):
        raise NotImplementedError("Fragment shader builder not implemented.")

    def generate_input_tuple(self, arr, tuple_type):
        if len(arr) == 0:
            return None
        out_t = []
        out_n = []
        for v_type, v_name in arr:
            out_t.append(v_type)
            out_n.append(v_name)
        return (f"{' '.join(out_t)} {tuple_type}", *out_n)