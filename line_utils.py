from vector3 import Vector3
from lineR import LineR

import math
import random

def circle_pts(sections, radius):
    theta = (2*math.pi)/sections
    out = []
    for num in range(sections):
        out.append(Vector3(radius*math.cos(theta*num), radius*math.sin(theta*num), 0.0))
    out.append(out[0])
    return out

def random_pts(sections):
    out = []
    for num in range(sections):
        out.append(Vector3(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))
    return out

def straight_line_pts(sections, vfrom, vto):
    out = []
    to_part = (vto - vfrom) / sections
    for num in range(sections + 1):
        out.append(vfrom + to_part*num)
    return out

def create_grid(grid_from, grid_to, grid_increment, sections):
    grid = []

    for i in range(grid_from, 0, grid_increment):
        line = LineR(
            straight_line_pts(sections, Vector3(i,grid_from,0), Vector3(i,grid_to+1,0)),
            0.01,
            (0.75,0.75,0.75)
        )
        grid.append(line)

    for i in range(1, grid_to + 1, grid_increment):
        line = LineR(
            straight_line_pts(sections, Vector3(i,grid_from,0), Vector3(i,grid_to+1,0)),
            0.01,
            (0.75,0.75,0.75)
        )
        grid.append(line)

    for i in range(grid_from, 0, grid_increment):
        line = LineR(
            straight_line_pts(sections, Vector3(grid_from,i,0), Vector3(grid_to+1,i,0)),
            0.01,
            (0.75,0.75,0.75)
        )
        grid.append(line)

    for i in range(1, grid_to + 1, grid_increment):
        line = LineR(
            straight_line_pts(sections, Vector3(grid_from,i,0), Vector3(grid_to+1,i,0)),
            0.01,
            (0.75,0.75,0.75)
        )
        grid.append(line)

    line = LineR(
        straight_line_pts(sections, Vector3(0,0,grid_from), Vector3(0,0,grid_to)),
        0.01,
        (1.0,0.0,0.0)
    )
    grid.append(line)

    line = LineR(
        straight_line_pts(sections, Vector3(0,grid_from,0), Vector3(0,grid_to,0)),
        0.01,
        (0.0,1.0,0.0)
    )
    grid.append(line)

    line = LineR(
        straight_line_pts(sections, Vector3(grid_from,0,0), Vector3(grid_to,0,0)),
        0.01,
        (0.0,0.0,1.0)
    )
    grid.append(line)

    return grid
