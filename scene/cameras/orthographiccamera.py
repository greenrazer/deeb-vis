from scene.cameras.camera import Camera

from base.matrix4 import Matrix4

class OrthographicCamera(Camera):
    def __init__(self, position, top, left, bottom, right, near, far):
        Camera.__init__(self, position)
        self.update(top, left, bottom, right, near, far)

    def update(self, top, left, bottom, right, near, far):
        self.proj_stale = True
        a = 2/(right-left)
        b = 2/(top-bottom)
        c = -2/(far-near)
        d = -(right+left)/(right-left)
        e = -(top+bottom)/(top-bottom)
        f = -(far+near)/(far-near)

        self.proj_mat =  Matrix4(
            a, 0.0, 0.0, 0.0,
            0.0, b, 0.0, 0.0,
            0.0, 0.0, c, 0.0,
            d, e, f, 1.0
        )

        self.mat = self.pos_mat @ self.proj_mat