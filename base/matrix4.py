import math
import numpy as np

from base.matrix import Matrix

class Matrix4(Matrix):
    def __init__(self,a,b,c,d, e,f,g,h, i,j,k,l, m,n,o,p):
        Matrix.__init__(self,(4,4))
        self._vals = np.array(
            [
                [a,b,c,d],
                [e,f,g,h],
                [i,j,k,l],
                [m,n,o,p]
            ]
        )
        self._cls = Matrix4

    @staticmethod
    def identity():
        return Matrix4 (
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        )
