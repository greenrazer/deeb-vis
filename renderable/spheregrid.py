import math


from base.vector3 import Vector3
from renderable.renderable import Renderable
from renderable.sphere import Sphere
from util import frange

def cart_to_polar(a, max_g):
    theta = math.atan2(a[1],a[0])
    return (math.hypot(a[0], a[1])/max_g, theta % 2.0*math.pi)

def color_wheel(radius, theta):
    h = theta
    s = -math.exp(-3.0*radius) + 1.0
    v = 1.0

    c = v*s
    x = c*(1-abs((3*theta/math.pi % 2) - 1))
    m = v - c

    if(0.0 <= theta and theta < math.pi/3.0):
        rgbprime = (c,x,0.0)
    elif(theta < 2.0*math.pi/3.0):
        rgbprime = (x,c,0.0)
    elif(theta < math.pi):
        rgbprime = (0.0,c,x)
    elif(theta < 4.0*math.pi/3.0):
        rgbprime = (0.0,x,c)
    elif(theta < 5.0*math.pi/3.0):
        rgbprime = (x,0.0,c)
    elif(theta < 2.0*math.pi):
        rgbprime = (c,0.0,x)

    return ((rgbprime[0] + m),
            (rgbprime[1] + m),
            (rgbprime[2] + m))


class SphereGrid(Renderable):
    def __init__(self, grid_from, grid_to, grid_increment=1, radius = 0.1, sections=2):
        Renderable.__init__(self)
        self.spheres = []
        self.create_grid(grid_from, grid_to, grid_increment, radius, sections)
    
    def transform(self, func):
        for i in range(len(self.spheres)):
            self.spheres[i] = func(self.spheres[i])

    def in_place_transform(self, func):
        for i in range(len(self.spheres)):
            func(self.spheres,i)

    def animate_transform(self, func, time):
        for i in range(len(self.spheres)):
            to = func(self.spheres[i].location)
            self.spheres[i].animate_to(to, time)
    
    def create_grid(self, grid_from, grid_to, grid_increment, radius, sections): 
        for i in frange(grid_from, grid_to+grid_increment, grid_increment):
            for j in frange(grid_from, grid_to+grid_increment, grid_increment):
                polar = cart_to_polar((i,j), grid_to)
                cw = color_wheel(polar[0], polar[1])
                self.spheres.append(
                    Sphere(
                        radius, 
                        Vector3(i,j,0.0), 
                        cw
                    )
                )


    @property
    def shader_info(self):
        shader_data = []
        nums = 0
        for sphere in self.spheres:
            vals, num = sphere.shader_info
            nums += num
            shader_data.extend(vals)
        
        return (shader_data, nums)