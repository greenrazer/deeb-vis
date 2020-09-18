import numpy as np

import numpy as np

from base.vector import Vector

class Matrix:
    def __init__(self, shape, *args):
        if len(args) > 0:
            self._vals = np.array(args).reshape(shape)
            self._cls = lambda *args: Matrix(shape, *args)

    def __str__(self):
        return str(self._vals)

    def __getitem__(self, at):
        return Vector.from_array(self._vals[at])

    def __matmul__(self, other):
        out = self._vals @ other._vals
        if isinstance(other, Matrix):
            return self.to_mat(out)
        else:
            return other.from_array(out)

    def __imatmul__(self, other):
        self._vals = self._vals @ other._vals
        return self

    def svd(self):
        u, s, uv = numpy.linalg.svd(self._vals)
        return (self.to_mat(u), self.to_mat(s), self.to_mat(uv))

    def to_mat(self, arr):
        if arr.shape != self.shape:
            return Matrix(arr.shape, *list(arr.flatten()))
        else:
            return self._cls(*list(arr.flatten()))
    
    def to_tuple(self):
        return tuple(self._vals.flatten())
    
    def transpose(self):
        self._vals = self._vals.transpose()
        return self

    def pad_to(self, dim):
        bottom = dim - self.shape[0]
        right = dim - self.shape[1]
        if bottom < 0 or right < 0:
            raise RuntimeError(f"Cannot pad to {self.shape} array to ({dim},{dim})")
        v = np.pad(self._vals, ((0,bottom), (0,right)))
        return(self.to_mat(v))
    
    def transposed(self):
        return self.to_mat(self._vals.transpose())

    def copy(self):
        return self.to_mat(self._vals)

    @property
    def shape(self):
        return self._vals.shape

    @staticmethod
    def from_array(arr):
        return Matrix(arr.shape, *list(arr.flatten()))

    @staticmethod
    def random(from_n, to_n, shape):
        random_arr = np.random.rand(*shape) * (to_n - from_n) + from_n
        return Matrix.from_array(random_arr)