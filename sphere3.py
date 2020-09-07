from vector3 import Vector3
from triangle3 import Triangle3
from trianglecollection import TriangleCollection

import math

def set_arr(arr, ind, arr2):
    for i in range(len(arr2)):
        arr[ind+i] = arr2[i]


class Sphere3:
    f = (1 + 5 ** 0.5) / 2

    init_verts = (
        -1, f, 0, 1, f, 0, 
        -1, -f, 0, 1, -f, 0, 
        0, -1, f, 0, 1, f, 
        0, -1, -f, 0, 1, -f, 
        f, 0, -1, f, 0, 1, 
        -f, 0, -1, -f, 0, 1
    )

    init_tris = (
        0, 11, 5, 0, 5, 1, 0, 1, 7, 0, 
        7, 10, 0, 10, 11, 11, 10, 2, 5, 11, 
        4, 1, 5, 9, 7, 1, 8, 10, 7, 6, 
        3, 9, 4, 3, 4, 2, 3, 2, 6, 3, 
        6, 8, 3, 8, 9, 9, 8, 1, 4, 9, 
        5, 2, 4, 11, 6, 2, 10, 8, 6, 7
    )

    def __init__(self, radius, location, subdivisions = 3):
        self.subdivisions = subdivisions

        self.triangles = self.generate_unit_icosphere(self.subdivisions)

        self.radius = radius
        self.location = location

    def _add_mid_point(self, a, b, verts, mid_cache, v):
        key = math.floor((a + b) * (a + b + 1) / 2) + min(a, b)
        if key in mid_cache:
            i = mid_cache[key]
            del mid_cache[key]
            return (i, v)
        mid_cache[key] = v
        for k in range(3):
            verts[3 * v + k] = (verts[3 * a + k] + verts[3 * b + k]) / 2
        return (v, v+1)

    def generate_unit_icosphere(self, subdivisions):
        T = 4 ** subdivisions
        verts = [0 for i in range((10 * T + 2) * 3)]
        set_arr(verts, 0, self.init_verts)

        tris = self.init_tris

        v = 12

        mid_cache = None if subdivisions == 0 else {}


        for i in range(subdivisions):
            # subdivide each triangle into 4 triangles
            triangles_next = [0 for _ in range(len(tris)*4)]
            for k in range(0,len(tris), 3):
                v1 = tris[k]
                v2 = tris[k+1]
                v3 = tris[k+2]
                (a, v) = self._add_mid_point(v1, v2, verts, mid_cache, v)
                (b, v) = self._add_mid_point(v2, v3, verts, mid_cache, v)
                (c, v) = self._add_mid_point(v3, v1, verts, mid_cache, v)
                set_arr(triangles_next, k*4, [v1, a, c, v2, b, a, v3, c, b, a, b, c])
            tris = triangles_next

        verts_temp = []
        for i in range(0,len(verts),3):
            curr_vert = Vector3(verts[i], verts[i + 1], verts[i + 2])
            verts_temp.append(curr_vert.normalize())

        triangles = []
        for k in range(0,len(tris), 3):
            v1 = verts_temp[tris[k + 0]]
            v2 = verts_temp[tris[k + 1]]
            v3 = verts_temp[tris[k + 2]]
            triangles.append(Triangle3(v1, v2, v3))

        return triangles
    
    def scale(self, sf):
        self.radius *= sf

    def translate(self, location):
        self.location += location



    


