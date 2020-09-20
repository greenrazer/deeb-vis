from base.vector3 import Vector3
from scene.objects.line import Line
from scene.objects.transformablesceneobject import TransformableSceneObject
from utils.util import frange


class LineGrid(TransformableSceneObject):
    floats_per_vertex = Line.floats_per_vertex
    chars_per_vertex = Line.chars_per_vertex
    bytes_per_vertex = Line.bytes_per_vertex
    def __init__(self, grid_from, grid_to, grid_increment=1, sections=100, width = 0.0005):
        TransformableSceneObject.__init__(self)
        self.grid = self.create_grid(grid_from, grid_to, grid_increment, sections, width)

    def straight_line_pts(self, sections, vfrom, vto):
        out = []
        to_part = (vto - vfrom) / sections
        for num in range(sections + 1):
            out.append(vfrom + to_part*num)
        return out

    def create_grid(self, grid_from, grid_to, grid_increment, sections, width):
        grid = []

        for i in frange(grid_from, 0, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(i,grid_from,0), Vector3(i,grid_to,0)),
                width,
                (0.0,0.0,0.0),
                True
            )
            grid.append(line)

        for i in frange(1, grid_to + 1, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(i,grid_from,0), Vector3(i,grid_to,0)),
                width,
                (0.0,0.0,0.0),
                True
            )
            grid.append(line)

        for i in frange(grid_from, 0, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(grid_from,i,0), Vector3(grid_to,i,0)),
                width,
                (0.0,0.0,0.0),
                True
            )
            grid.append(line)

        for i in frange(1, grid_to + 1, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(grid_from,i,0), Vector3(grid_to,i,0)),
                width,
                (0.0,0.0,0.0),
                True
            )
            grid.append(line)

        line = Line(
            self.straight_line_pts(sections, Vector3(0,grid_from,0), Vector3(0,grid_to,0)),
            width,
            (0.0,0.75,0.0),
            True
        )
        grid.append(line)

        line = Line(
            self.straight_line_pts(sections, Vector3(grid_from,0,0), Vector3(grid_to,0,0)),
            width,
            (0.0,0.0,0.75),
            True
        )
        grid.append(line)

        return grid

    @property
    def num_verts(self):
        verts = 0
        for g in self.grid:
            verts += g.num_verts
        return verts
    
    @property
    def shader_info(self):
        shader_data = []
        for line in self.grid:
            verts = line.shader_info
            shader_data.extend(verts)
        
        return shader_data
