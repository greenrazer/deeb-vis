import struct

class Renderable:
    def __init__(self):
        self.cache = None
        self.use_chache = False

    def to_bytes(self):
        verts, num = self.shader_info
        buf = struct.pack('<'+'16f1B' * num , *verts)
        self.cache = buf
        return buf