class BufferBuilder:
    object_cls = None

    def __init__(self, object_list):
        self.objs = self.get_objs(object_list)
        self.program_builder = self.get_program_builder()
        self.program = None
        self.built = False

    def get_objs(self, object_list):
        out = []
        for i in object_list:
            if self.is_correct_class(i):
                out.append(i)
        return out

    @property
    def populated(self):
        return len(self.objs) > 0

    @property
    def num_verts(self):
        verts = 0
        for s in self.objs:
            verts += s.num_verts
        return verts

    def get_program_builder(self):
        raise NotImplementedError()

    def is_correct_class(self, instance):
        raise NotImplementedError()

    def get_bytes(self):
        buf = bytearray(self.num_verts*self.object_cls.bytes_per_vertex)
        at = 0
        for s in self.objs:
            to_write = s.to_bytes()
            buf[at:at+len(to_write)] = to_write
            at += len(to_write)
        return buf

    def set_uniform(self, uniform_name, value):
        if not self.built:
            raise RuntimeError("Must build shaders before attaching to uniforms")
        if self.program and uniform_name in self.program_builder.uniforms:
            self.program[uniform_name].value = value

    def build(self, context):
        self.built = True
        s = self.get_bytes()
        if len(s) == 0:
            return None
        vbo = context.buffer(s)
        self.program = self.program_builder.build(context)
        per_vertex_args = self.program_builder.input_tuple_per_vertex

        return context.vertex_array(self.program, [
            (vbo, *per_vertex_args),
        ])
