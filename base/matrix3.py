import random
import numpy as np

from base.matrix import Matrix
from base.vector3 import Vector3

class Matrix3(Matrix):
    def __init__(self,a,b,c, d,e,f, g,h,i):
        Matrix.__init__(self)
        self._vals = np.array(
            [
                [a,b,c],
                [d,e,f],
                [g,h,i]
            ]
        )
        self._cls = Matrix3
    
    @staticmethod
    def identity():
        return Matrix3(1,0,0,0,1,0,0,0,1)
    
    @staticmethod
    def random(from_n, to_n):
        return Matrix3(
            random.uniform(from_n,to_n),random.uniform(from_n,to_n),random.uniform(from_n,to_n),
            random.uniform(from_n,to_n),random.uniform(from_n,to_n),random.uniform(from_n,to_n),
            random.uniform(from_n,to_n),random.uniform(from_n,to_n),random.uniform(from_n,to_n)
        )


