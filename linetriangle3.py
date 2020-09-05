class LineTrianglePair3:
    data = (((0, 1, 0), (0, 1, 1)), ((0, 1, 1), (0, 1, 0)))
    def __init__(self, v1, v2, t1, t2, width):
        self.verts = [v1, v2]
        self.tans = [t1, t2]
        self.widths = [-width, width]
    
    def __iter__(self):
        self.at = 0
        return self
    
    def __next__(self):
        if self.at == 2:
            raise StopIteration
        
        curr = self.data[self.at]
        self.at += 1
        return [
            self.verts[curr[0][0]],  self.verts[curr[0][1]],  self.verts[curr[0][2]],
            self.tans[curr[0][0]],   self.tans[curr[0][1]],   self.tans[curr[0][2]],
            self.widths[curr[1][0]], self.widths[curr[1][1]], self.widths[curr[1][2]]
        ]
