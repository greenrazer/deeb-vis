import struct

class Renderable:
    def to_bytes(self):
        buf = bytes()
        for val in self.shader_info:
            buf += struct.pack('10f1B', *val)
        return buf