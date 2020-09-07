from base.vector3 import Vector3

class Triangle3:
    def __init__(self, v1, v2, v3):
        self._verticies = [v1, v2, v3]

    def __iter__(self):
        return iter(self._verticies)

    def __add__(self, other):
        temp = self.copy()
        temp += other
        return temp

    def __iadd__(self, other):
        for i in range(len(self._verticies)):
            self._verticies[i] += other
        return self

    def __mul__(self, other):
        temp = self.copy()
        temp *= other
        return temp
    
    def __imul__(self, other):
        for i in range(len(self._verticies)):
            self._verticies[i] *= other
        return self

    def __truediv__(self, other):
        temp = self.copy()
        temp /= other
        return temp

    def __idiv__(self, other):
        for i in range(len(self._verticies)):
            self._verticies[i] /= other
        return self

    def normal(self):
        return (v2 - v1).cross(v3 - v1)

    def copy(self):
        return Triangle3(self._verticies[0].copy(), self._verticies[1].copy(), self._verticies[2].copy())




def test_Triangle3():
    pass



if __name__ == "__main__":
    test_Triangle3()
    
