import numpy as np

from base.vector import Vector

class Matrix:
    def __init__(self):
        self.values = []

    def _assert_check_mat_size(self, other):
        if self.size[1] != other.size[0]:
            raise Exception(f"{self.__class__.__name__} cannot be compared with {other.__class__.__name__}")

    def __matmul__(self, other):
        self._assert_check_mat_size(other)
        if isinstance(other, Vector):
            return other._cls(self.values[0] @ other, self.values[1] @ other, self.values[2] @ other)
        else:
            o = other.transpose()
            return self._cls(self.values[0] @ other[0], self.values[0] @ other[1], self.values[0] @ other[2],
                             self.values[1] @ other[0], self.values[1] @ other[1], self.values[1] @ other[2],
                             self.values[2] @ other[0], self.values[2] @ other[1], self.values[2] @ other[2])

    def __imatmul__(self, other):
        self._assert_check_mat_size(other)
        o = other.transpose()
        self.values = [self._vec_cls(self.values[0] @ other[0], self.values[0] @ other[1], self.values[0] @ other[2]),
                        self._vec_cls(self.values[1] @ other[0], self.values[1] @ other[1], self.values[1] @ other[2]),
                        self._vec_cls(self.values[2] @ other[0], self.values[2] @ other[1], self.values[2] @ other[2])]
    
    def to_array(self):
        out = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                out[i][j] = self.values[i][j]
        return np.array(out)

    def from_array(self, arr):
        self.values = self._cls(*arr.flatten().tolist()).values

    def svd(self):
        arr = self.to_array()
        u, s, uv = numpy.linalg.svd(arr)


    def transpose(self):
        out = [self._vec_cls(*([0]*self.size[0])) for _ in range(self.size[1])]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                out[j][i] = self.values[i][j]
        return out

        
    @property
    def size(self):
        return (0,0)