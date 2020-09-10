import math
import numpy as np

from base.matrix import Matrix

class Matrix4(Matrix):

    def __init__(self,a,b,c,d, e,f,g,h, i,j,k,l, m,n,o,p):
        Matrix.__init__(self)
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
    def perspective_projection(z_near, z_far, ratio, fovy):
        zmul = (-2.0 * z_near * z_far) / (z_far - z_near)
        ymul = 1.0 / math.tan(fovy / 2)
        xmul = ymul / ratio

        return Matrix4(
            -xmul, 0.0, 0.0, 0.0,
            0.0, ymul, 0.0, 0.0,
            0.0, 0.0, -1.0, -1.0,
            0.0, 0.0, zmul, 0.0
        )
    
    @staticmethod
    def orthographic_projection(top, left, bottom, right, near, far):
        a = 2/(right-left)
        b = 2/(top-bottom)
        c = -2/(far-near)
        d = -(right+left)/(right-left)
        e = -(top+bottom)/(top-bottom)
        f = -(far+near)/(far-near)

        return Matrix4(
            a, 0.0, 0.0, 0.0,
            0.0, b, 0.0, 0.0,
            0.0, 0.0, c, 0.0,
            d, e, f, 1.0
        )
