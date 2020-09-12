import struct

class SceneObject:
    floats_per_vertex = 24
    chars_per_vertex = 1

    bytes_per_vertex = floats_per_vertex*4 + chars_per_vertex*1

    def __init__(self):
        self.cache = None
        self.use_chache = False

    def to_bytes(self):
        verts = self.shader_info
        vertex_unit = f'{self.floats_per_vertex}f{self.chars_per_vertex}B'
        buf = struct.pack('<' + vertex_unit * self.num_verts , *verts)
        self.cache = buf
        return buf