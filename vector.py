import math

class Vector:
    def __getitem__(self, ind):
        return self._vec[ind]

    def __setitem__(self, ind, val):
        self._vec[ind] = val
    
    def __len__(self):
        return len(self._vec)
    
    def _assert_check_vec_size(self,other):
        if(len(self) != len(other)):
            raise Exception(f"{self.__class__.__name__} cannot be compared with {other.__class__.__name__}")

    def __iter__(self):
        return iter(self._vec)

    def __lt__(self, other):
        self._assert_check_vec_size(other)
        return self.length() < other.length()

    def __le__(self, other):
        self._assert_check_vec_size(other)
        return self.length() <= other.length()

    def __gt__(self, other):
        self._assert_check_vec_size(other)
        return self.length() > other.length()

    def __ge__(self, other):
        self._assert_check_vec_size(other)
        return self.length() >= other.length()

    def __eq__(self, other):
        self._assert_check_vec_size(other)
        return self._vec == other._vec 
    
    def __ne__(self, other):
        self._assert_check_vec_size(other)
        return self._vec != other._vec 

    def __add__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            out = []
            for i in range(len(self)):
                out.append(self[i] + other[i])
            return self._cls(*out)
        else:
            out = []
            for i in range(len(self)):
                out.append(self[i] + other)
            return self._cls(*out)

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            for i in range(len(self)):
                self[i] += other[i]
        else:
            for i in range(len(self)):
                self[i] += other
        return self

    def __sub__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            out = []
            for i in range(len(self)):
                out.append(self[i] - other[i])
            return self._cls(*out)
        else:
            out = []
            for i in range(len(self)):
                out.append(self[i] - other)
            return self._cls(*out)

    def __isub__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            for i in range(len(self)):
                self[i] -= other[i]
        else:
            for i in range(len(self)):
                self[i] -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            out = []
            for i in range(len(self)):
                out.append(self[i] * other[i])
            return self._cls(*out)
        else:
            out = []
            for i in range(len(self)):
                out.append(self[i] * other)
            return self._cls(*out)

    def __imul__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            for i in range(len(self)):
                self[i] *= other[i]
        else:
            for i in range(len(self)):
                self[i] *= other
        return self

    def __matmul__(self, other):
        self._assert_check_vec_size(other)
        out = 0
        for i in range(len(self)):
            out += self[i] * other[i]
        return out

    def __truediv__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            out = []
            for i in range(len(self)):
                out.append(self[i] / other[i])
            return self._cls(*out)
        else:
            out = []
            for i in range(len(self)):
                out.append(self[i] / other)
            return self._cls(*out)

    def __idiv__(self, other):
        if isinstance(other, Vector):
            self._assert_check_vec_size(other)
            for i in range(len(self)):
                self[i] /= other[i]
        else:
            for i in range(len(self)):
                self[i] /= other
        return self

    def __neg__(self):
        out = []
        for i in range(len(self)):
            out.append(-self[i])
        return self._cls(*out)
    
    def __str__(self):
        out = [str(i) for i in self]
        return "[" + ", ".join(out) + "]"

    def normalized(self):
        return self / self.length()

    def normalize(self):
        self /= self.length()
        return self

    def length(self):
        return math.sqrt(sum(self * self))
    
    def copy(self):
        return self._cls(*self._vec)


