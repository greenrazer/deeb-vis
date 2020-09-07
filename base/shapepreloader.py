import pickle

from base.vector3 import Vector3
from base.triangle3 import Triangle3

def get_ico_sphere(subdivisions):
        with open(f'shapes/icosphere_sub{subdivisions}.data', 'rb') as f:
            triangles_pkl = pickle.load(f)
            triangles = []
            for t in triangles_pkl:
                triangles.append(
                    Triangle3(
                        Vector3(t[0][0], t[0][1], t[0][2]),
                        Vector3(t[1][0], t[1][1], t[1][2]),
                        Vector3(t[2][0], t[2][1], t[2][2])
                    )
                )
            return triangles


class ShapePreloader:
    icosphere = [
        get_ico_sphere(0),
        get_ico_sphere(1),
        get_ico_sphere(2),
        get_ico_sphere(3)
    ]