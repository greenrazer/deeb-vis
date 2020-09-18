from scene.objects.transformablesceneobject import TransformableSceneObject
from base.line3 import Line3
from base.vector3 import Vector3

class Vector(TransformableSceneObject, Line3):
    def __init__(self, verticies, width, color = None, animated = False, last_n=0, head_thickeness_multiplier=3):
        Line3.__init__(self, verticies, width)
        TransformableSceneObject.__init__(self)

        self.last_n = last_n
        self.head_thickeness_multiplier = head_thickeness_multiplier

        self.animated_line_types = [8,9,10]
        self.static_line_types = [5, 6, 7]

        self.animated = animated
        self.color = color

        self.color_array = [
            [1.0,0.0,0.0],
            [0.0,1.0,0.0],
            [0.0,0.0,1.0],
            [1.0,1.0,0.0],
            [0.0,1.0,1.0],
            [1.0,0.0,1.0],
        ]
        self.c = 0
    
    def get_type(self, val):
        if self.animated:
            return self.animated_line_types[val]
        else:
            return self.static_line_types[val]

    @staticmethod
    def straight_vector(from_v, to_v, head_size, width, head_thickeness_multiplier=3, color=(1.0,0.0,0.0)):
        straight_end = to_v - (to_v - from_v).normalize() * head_size
        return Vector(
            [from_v, straight_end, to_v], 
            width, 
            last_n=1, 
            head_thickeness_multiplier = head_thickeness_multiplier, 
            color=color)

    @property
    def shader_info(self):
        shader_data = []
        triangle_pair_data = self.generate_triangle_pairs()
        vert = 0
        for triangle_pair in triangle_pair_data:
            switch_section = len(triangle_pair_data) - self.last_n
            if vert >= switch_section:
                mult_b4 = 1.0 - (vert - switch_section)/(self.last_n)
                mult_aft = 1.0 - (vert + 1 - switch_section)/(self.last_n)
                b4_width_mult = self.head_thickeness_multiplier*mult_b4
                aft_width_mult = self.head_thickeness_multiplier*mult_aft
            else:
                b4_width_mult = 1.0
                aft_width_mult = 1.0
            
            triangle_pair.modify_widths(b4_width_mult, aft_width_mult)

            for triangle in triangle_pair:
                color = self.color_array[self.c] if self.color is None else self.color
                shader_data.extend([
                    triangle[0][0],triangle[0][1],triangle[0][2], 0.0,0.0,0.0, triangle[3][0],triangle[3][1],triangle[3][2], triangle[6][0],triangle[6][1],triangle[6][2], 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,   0.0,0.0,0.0,   0.0,0.0,0.0,  triangle[9], color[0],color[1],color[2],   self.get_type(triangle[12]),
                    triangle[1][0],triangle[1][1],triangle[1][2], 0.0,0.0,0.0, triangle[4][0],triangle[4][1],triangle[4][2], triangle[7][0],triangle[7][1],triangle[7][2], 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,   0.0,0.0,0.0,   0.0,0.0,0.0,  triangle[10], color[0],color[1],color[2],  self.get_type(triangle[13]),
                    triangle[2][0],triangle[2][1],triangle[2][2], 0.0,0.0,0.0, triangle[5][0],triangle[5][1],triangle[5][2], triangle[8][0],triangle[8][1],triangle[8][2], 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,   0.0,0.0,0.0,   0.0,0.0,0.0,  triangle[11], color[0],color[1],color[2],  self.get_type(triangle[14])
                ])
                self.c = (self.c + 1) % 6
            vert += 1
        return shader_data
    