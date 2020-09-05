from vector3 import Vector3

class Triangle3:
    def __init__(self, v1, v2, v3):
        self._verticies = [v1, v2, v3]

    def normal(self):
        return (v2 - v1).cross(v3 - v1)

    def __iter__(self):
        return iter(self._verticies)



def test_Triangle3():
    pass



if __name__ == "__main__":
    test_Triangle3()
    
