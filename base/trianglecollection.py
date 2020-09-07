class TriangleCollection:
    def __init__(self, triangles):
        self._triangles = triangles

    def __iter__(self):
        return iter(self._triangles)

    def __add__(self, other):
        temp = self.copy()
        temp += other
        return temp

    def __iadd__(self, other):
        for i in range(len(self._triangles)):
            self._triangles[i] += other
        return self

    def __mul__(self, other):
        temp = self.copy()
        temp *= other
        return temp
    
    def __imul__(self, other):
        for i in range(len(self._triangles)):
            self._triangles[i] *= other
        return self

    def __truediv__(self, other):
        temp = self.copy()
        temp /= other
        return temp

    def __idiv__(self, other):
        for i in range(len(self._triangles)):
            self._triangles[i] /= other
        return self

    def copy(self):
        output = []
        for tri in self._triangles:
            output.append(tri.copy())
        return TriangleCollection(output)