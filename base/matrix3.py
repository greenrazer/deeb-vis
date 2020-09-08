import random

from base.matrix import Matrix
from base.vector3 import Vector3

class Matrix3(Matrix):
    _vec_cls = Vector3

    def __init__(self,a,b,c,d,e,f,g,h,i):
        Matrix.__init__(self)
        self.values = [
            Vector3(a,b,c),
            Vector3(d,e,f),
            Vector3(g,h,i)
        ]
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

    @property
    def size(self):
        return (3,3)


