from base.linetriangle3 import LineTriangle3, VertexPosition
from base.vector3 import Vector3

class Line3:
    def __init__(self, line, width):
        self._line = line
        self.width = width
        self.triangle_pairs_cache = self.generate_triangle_pairs()

    def __len__(self):
        return len(self._line)

    @property
    def num_verts(self):
        return len(self.triangle_pairs_cache) * 6

    def copy(self):
        out = []
        for l in self.line:
            out.append(l.copy())
        return Line3(out, width)

    def transform(self, func):
        for v in range(len(self)):
            self._line[v] = func(self._line[v])

    def tangent(self, at):
        if(at == 0):
            vertex_at = self._line[at]
            vertex_at_next = self._line[at + 1]
            return (vertex_at_next - vertex_at).normalize()
        elif(at == len(self._line)-1):
            vertex_at_prev = self._line[at - 1]
            vertex_at = self._line[at]
            return (vertex_at - vertex_at_prev).normalize()
        else:
            vertex_at_prev = self._line[at - 1]
            vertex_at = self._line[at]
            vertex_at_next = self._line[at + 1]

            v1 = (vertex_at_prev - vertex_at).normalize()
            v2 = (vertex_at_next - vertex_at).normalize()

            dot = v1 @ v2
            if abs(dot) == 1.0:
                return v2
            
            return (v2 - v1).normalize()

    def ind_to_pos(self, at):
        if at == 0:
            return VertexPosition.START
        elif at < len(self._line)-1:
            return VertexPosition.MIDDLE
        else:
            return VertexPosition.END

    def generate_triangle_pairs(self):
        self.triangles = []
        for i in range(len(self._line)-1):

            prev = Vector3(0.0,0.0,0.0) if i == 0 else self._line[i-1]
            nxt = Vector3(0.0,0.0,0.0) if i == len(self._line)-2 else self._line[i+2]
            self.triangles.append(LineTriangle3(
                prev, self._line[i], self._line[i+1], nxt,
                self.ind_to_pos(i), self.ind_to_pos(i+1),
                self.width))
        return self.triangles

            



    

