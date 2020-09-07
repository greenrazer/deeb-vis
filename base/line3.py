from base.linetriangle3 import LineTrianglePair3
from base.triangle3 import Triangle3

class Line3:
    def __init__(self, line, width):
        self._line = line
        self.width = width

    def __len__(self):
        return len(self._line)

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
    
    def generate_triangle_pairs(self):
        self.triangles = []
        self.tan_queue = [self.tangent(0)]
        for i in range(len(self._line)-1):
            self.tan_queue.append(self.tangent(i+1))
            self.triangles.append(LineTrianglePair3(self._line[i], self._line[i+1], self.tan_queue[i], self.tan_queue[i+1], self.width))
        
        return self.triangles

            



    

