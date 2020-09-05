from vector import Vector

class Vector3(Vector):
    def __init__(self, x, y, z):
        self._vec = [x,y,z]
        self._cls = Vector3 

    def __getattr__(self, key):
        output = []

        for c in key:
            if c not in 'xyz':
                raise Exception(f"Cannot access .{c} on {self.__class__.__name__}.")
            if c == 'x':
                output.append(self.x)
            elif c == 'y':
                output.append(self.y)
            elif c == 'z':
                output.append(self.z)
        
        if len(output) == 1:
            return output[0]
        elif len(output) == 3:
            return Vector3(*output)
        else:
            return output
        
    @property
    def x(self):
        return self._vec[0]

    @x.setter
    def x(self, val):
        self._vec[0] = val

    @property
    def y(self):
        return self._vec[1]

    @y.setter
    def y(self, val):
        self._vec[1] = val

    @property
    def z(self):
        return self._vec[2]

    @z.setter
    def z(self, val):
        self._vec[2] = val

    def cross(self, other):
        return self._cls(self[2]*other[3] - self[3]*other[2], 
                         self[3]*other[1] - self[1]*other[3], 
                         self[1]*other[2] - self[2]*other[1])


def test_Vector3():
    print("Start testing Vector3.")
    v3 = Vector3(1,2,3)

    # Member Access
    assert v3.x == 1, "Cannot Access Memeber x"
    assert v3.y == 2, "Cannot Access Memeber y"
    assert v3.z == 3, "Cannot Access Memeber z"

    # Swizzle
    assert v3.xxx == Vector3(1,1,1), "Cannot swizzle xxx"
    assert v3.yyy == Vector3(2,2,2), "Cannot swizzle yyy"
    assert v3.zzz == Vector3(3,3,3), "Cannot swizzle zzz"
    assert v3.xyz == Vector3(1,2,3), "Cannot swizzle xyz"
    assert v3.zyxxyz == [3,2,1,1,2,3], "Cannot swizzle zyxxyz"

    # Operations
    assert v3 - v3 == Vector3(0,0,0), "Cannot subtract vector from itself"
    assert v3 + v3 == Vector3(2,4,6), "Cannot add vector to itself"
    assert v3 * v3 == Vector3(1,4,9), "Cannot multiply a vector by itself"
    assert v3 / v3 == Vector3(1,1,1), "Cannot divide a vector by itself"
    assert v3 @ v3 == 14, "Cannot matrix multiply vector by itself"

    assert v3 - 2 == Vector3(-1,0,1), "Cannot subtract vector from itself"
    assert v3 + 2 == Vector3(3,4,5), "Cannot add vector to itself"
    assert v3 * 2 == Vector3(2,4,6), "Cannot multiply a vector by itself"
    assert v3 / 2 == Vector3(0.5,1,1.5), "Cannot divide a vector by itself"

    v3 = Vector3(4,8,19)
    assert v3.length() == 21, "Length incorrect"

    v32 = Vector3(1,1,1)
    assert v3 > v32, "Comparison doesnt work"

    vec = v32.copy()
    vec += 1
    assert vec != v32, "Copy doesnt work"



    print("Finish testing Vector3.")

if __name__ == '__main__':
    test_vector3()