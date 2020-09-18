from base.vector3 import Vector3
from scene.objects.line import Line
from scene.objects.sceneobject import SceneObject
from utils.util import frange


class Grid(SceneObject):
    def __init__(self, grid_from, grid_to, grid_width=0.01, grid_increment=1, sections=1):
        SceneObject.__init__(self)
        self.grid = self.create_grid(grid_from, grid_to, grid_width, grid_increment, sections)

    def straight_line_pts(self, sections, vfrom, vto):
        out = []
        to_part = (vto - vfrom) / sections
        for num in range(sections + 1):
            out.append(vfrom + to_part*num)
        return out

    def create_grid(self, grid_from, grid_to, grid_width, grid_increment, sections):
        grid = []

        for i in frange(grid_from, 0, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(i,grid_from,0), Vector3(i,grid_to,0)),
                grid_width,
                (0.75,0.75,0.75)
            )
            grid.append(line)

        for i in frange(1, grid_to + 1, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(i,grid_from,0), Vector3(i,grid_to,0)),
                grid_width,
                (0.75,0.75,0.75)
            )
            grid.append(line)

        for i in frange(grid_from, 0, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(grid_from,i,0), Vector3(grid_to,i,0)),
                grid_width,
                (0.75,0.75,0.75)
            )
            grid.append(line)

        for i in frange(1, grid_to + 1, grid_increment):
            line = Line(
                self.straight_line_pts(sections, Vector3(grid_from,i,0), Vector3(grid_to,i,0)),
                grid_width,
                (0.75,0.75,0.75)
            )
            grid.append(line)

        line = Line(
            self.straight_line_pts(sections, Vector3(0,0,grid_from), Vector3(0,0,grid_to)),
            grid_width,
            (1.0,0.0,0.0)
        )
        grid.append(line)

        line = Line(
            self.straight_line_pts(sections, Vector3(0,grid_from,0), Vector3(0,grid_to,0)),
            grid_width,
            (0.0,1.0,0.0)
        )
        grid.append(line)

        line = Line(
            self.straight_line_pts(sections, Vector3(grid_from,0,0), Vector3(grid_to,0,0)),
            grid_width,
            (0.0,0.0,1.0)
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
