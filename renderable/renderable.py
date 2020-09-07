import struct

class Renderable:
    def __init__(self):
        self.cache = None
        self.use_chache = False

    def to_bytes(self):
        if self.use_chache:
            return self.cache
        else:
            buf = bytes()
            for val in self.shader_info:
                buf += struct.pack('16f1B', *val)
            self.cache = buf
            return buf