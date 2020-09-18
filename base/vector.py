import math
import random
import numpy as np

class Vector:
    def __init__(self, *args):
        self._vals = np.array(args)
        self._cls = Vector

    def __getitem__(self, ind):
        return self._vals[ind]

    def __setitem__(self, ind, val):
        self._vals[ind] = val
    
    def __len__(self):
        return len(self._vals)
    
    def _assert_check_vals_size(self,other):
        if self.shape != other.shape:
            raise Exception(f"{self.__class__.__name__} cannot be compared with {other.__class__.__name__}")

    def __iter__(self):
        return iter(self._vals)

    def __lt__(self, other):
        self._assert_check_vals_size(other)
        return self.length() < other.length()

    def __le__(self, other):
        self._assert_check_vals_size(other)
        return self.length() <= other.length()

    def __gt__(self, other):
        self._assert_check_vals_size(other)
        return self.length() > other.length()

    def __ge__(self, other):
        self._assert_check_vals_size(other)
        return self.length() >= other.length()

    def __eq__(self, other):
        self._assert_check_vals_size(other)
        return (self._vals == other._vals).all() 
    
    def __ne__(self, other):
        self._assert_check_vals_size(other)
        return not(self._vals != other._vals).all()

    def __add__(self, other):
        if isinstance(other, Vector):
            return self.from_vec(self._vals + other._vals)
        else:
            return self.from_vec(self._vals + other)

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self._vals = self._vals + other._vals
        else:
            self._vals = self._vals + other
        return self

    def __sub__(self, other):
        if isinstance(other, Vector):
            return self.from_vec(self._vals - other._vals)
        else:
            return self.from_vec(self._vals - other)

    def __isub__(self, other):
        if isinstance(other, Vector):
            self._vals = self._vals - other._vals
        else:
            self._vals = self._vals - other
        return self

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.from_vec(self._vals * other._vals)
        else:
            return self.from_vec(self._vals * other)

    def __imul__(self, other):
        if isinstance(other, Vector):
            self._vals = self._vals * other._vals
        else:
            self._vals = self._vals * other
        return self

    def __matmul__(self, other):
        return self._vals @ other._vals

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return self.from_vec(self._vals / other._vals)
        else:
            return self.from_vec(self._vals / other)

    def __idiv__(self, other):
        if isinstance(other, Vector):
            self._vals = self._vals / other._vals
        else:
            self._vals = self._vals / other
        return self

    def __neg__(self):
        return self.from_vec(-self._vals)
    
    def __str__(self):
        return str(self._vals)

    def normalized(self):
        return self / self.length()

    def normalize(self):
        self /= self.length()
        return self

    def length(self):
        return math.sqrt(sum(self * self))
    
    def copy(self):
        return self._cls(*self._vals)
    
    def from_vec(self, arr):
        return self._cls(*list(arr))

    def to_tuple(self):
        return tuple(self)

    def pad_to(self, size):
        v = self._vals
        if(len(self.shape) > 1):
            v = self._vals.flatten()
        vec = np.pad(v, (0, size - v.shape[0]))
        return self.from_vec(vec)

    @property
    def shape(self):
        return self._vals.shape

    @property
    def size(self):
        return self._vals.shape[0]


    @staticmethod
    def from_array(arr):
        return Vector(*list(arr))

    @staticmethod
    def random(from_n, to_n, size):
        vec = []
        for i in range(size):
            vec.append(random.uniform(from_n,to_n))
        return Vector(*vec)
