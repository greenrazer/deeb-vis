from base.matrix4 import Matrix4
from base.vector3 import Vector3

class Camera:
    def __init__(self, position):
        self.pos_mat = Matrix4.identity()
        self.proj_mat = Matrix4.identity()
        self.mat = Matrix4.identity()
        self._position = position
        self.pos_stale = True
        self.proj_stale = True

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self.pos_stale = True
        self._position = pos
        self.look_at(self.look_at_v, self.up)

    @property
    def projection(self):
        return self.mat
    
    def look_at(self, look_at, up):
        self.proj_stale = True
        self.look_at_v = look_at
        self.up = up

        forward = (look_at - self._position).normalize()
        side = forward.cross(up).normalize()
        upward = side.cross(forward)

        a = -self._position @ side
        b = -self._position @ upward
        c = self._position @ forward

        self.pos_mat =  Matrix4(
            side.x, upward.x, -forward.x, 0,
            side.y, upward.y, -forward.y, 0,
            side.z, upward.z, -forward.z, 0,
            a, b, c, 1
        )

        self.mat = self.pos_mat @ self.proj_mat