from base.line3 import Line3
from renderable.renderable import Renderable

class Line(Renderable, Line3):
    def __init__(self, verticies, width, color = None):
        Line3.__init__(self, verticies, width)
        Renderable.__init__(self)
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
    
    @property
    def shader_info(self):
        shader_data = []
        verts = 0
        triangle_pair_data = self.generate_triangle_pairs()
        for triangle_pair in triangle_pair_data:
            for triangle in triangle_pair:
                color = self.color_array[self.c] if self.color is None else self.color
                verts += 3
                shader_data.extend([
                    triangle[0][0],triangle[0][1],triangle[0][2], 0.0,0.0,0.0, triangle[3][0],triangle[3][1],triangle[3][2], 0.0,0.0,0.0, 0.0,0.0,   0.0,0.0,0.0,   0.0,0.0,0.0,  triangle[6], color[0],color[1],color[2],  0,
                    triangle[1][0],triangle[1][1],triangle[1][2], 0.0,0.0,0.0, triangle[4][0],triangle[4][1],triangle[4][2], 0.0,0.0,0.0, 0.0,0.0,   0.0,0.0,0.0,   0.0,0.0,0.0,  triangle[7], color[0],color[1],color[2],  0,
                    triangle[2][0],triangle[2][1],triangle[2][2], 0.0,0.0,0.0, triangle[5][0],triangle[5][1],triangle[5][2], 0.0,0.0,0.0, 0.0,0.0,   0.0,0.0,0.0,   0.0,0.0,0.0,  triangle[8], color[0],color[1],color[2],  0
                ])
                self.c = (self.c + 1) % 6
        return (shader_data, verts)
        