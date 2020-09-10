import numpy as np

import numpy as np

from base.vector import Vector

class Matrix:
    def __matmul__(self, other):
        out = self._vals @ other._vals
        return other.from_array(out)

    def __imatmul__(self, other):
        self._vals = self._vals @ other._vals

    def svd(self):
        u, s, uv = numpy.linalg.svd(self._vals)

    def from_array(self, arr):
        return self._cls(*list(arr.flatten()))

    def to_tuple(self):
        return tuple(self._vals.flatten())

    @property
    def shape(self):
        return self._vals.shape