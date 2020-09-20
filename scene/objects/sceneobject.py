import struct

class SceneObject:
    def __init__(self):
        self.animated = False
    
    def to_bytes(self):
        verts = self.shader_info
        if self.chars_per_vertex > 0:
            vertex_unit = f'{self.floats_per_vertex}f{self.chars_per_vertex}B'
        else:
            vertex_unit = f'{self.floats_per_vertex}f'
        buf = struct.pack('<' + vertex_unit * self.num_verts , *verts)
        return buf