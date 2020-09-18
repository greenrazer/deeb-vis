from enum import Enum

class VertexPosition(Enum):
    START = 0
    MIDDLE = 1
    END = 2

class LineTriangle3:
    data = (((0, 1, 0), (0, 1, 1)), ((0, 1, 1), (0, 1, 0)))
    def __init__(self, vm1, v0, v1, v2, v0type, v1type, width):
        self.verts = [v0, v1, v2, vm1]
        self.types = [v0type, v1type]
        self.widths = [-width, width]
        self.mod_widths = False

    def modify_widths(self, b4, aft):
        self.widths_mult = [b4, aft]
        self.mod_widths = True

    def __iter__(self):
        self.at = 0
        return self
    
    def __next__(self):
        if self.at == 2:
            raise StopIteration
        
        curr = self.data[self.at]
        self.at += 1
        if self.mod_widths:
            width_arr = [
                self.widths[curr[1][0]] * self.widths_mult[curr[0][0]], 
                self.widths[curr[1][1]] * self.widths_mult[curr[0][1]], 
                self.widths[curr[1][2]] * self.widths_mult[curr[0][2]]
            ]
        else:
            width_arr = [self.widths[curr[1][0]], self.widths[curr[1][1]], self.widths[curr[1][2]]]

        return [
                self.verts[curr[0][0]],  self.verts[curr[0][1]],  self.verts[curr[0][2]],
                self.verts[curr[0][0]-1],  self.verts[curr[0][1]-1],  self.verts[curr[0][2]-1],
                self.verts[curr[0][0]+1],  self.verts[curr[0][1]+1],  self.verts[curr[0][2]+1],
                *width_arr,
                self.types[curr[0][0]].value,  self.types[curr[0][1]].value,  self.types[curr[0][2]].value,
            ]
