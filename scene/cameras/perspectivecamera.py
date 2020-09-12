import math

from scene.cameras.camera import Camera

from base.matrix4 import Matrix4

class PerspectiveCamera(Camera):
    def __init__(self, position, z_near, z_far, ratio, fovy):
        Camera.__init__(self, position)
        self.update(z_near, z_far, ratio, fovy)
    
    def update(self, z_near, z_far, ratio, fovy):
        self.proj_stale = True
        self.z_near = z_near
        self.z_far = z_far
        self.ratio = ratio
        self.fovy = fovy

        zmul = (-2.0 * z_near * z_far) / (z_far - z_near)
        ymul = 1.0 / math.tan(fovy / 2)
        xmul = ymul / ratio

        self.proj_mat =  Matrix4(
            -xmul, 0.0, 0.0, 0.0,
            0.0, ymul, 0.0, 0.0,
            0.0, 0.0, -1.0, -1.0,
            0.0, 0.0, zmul, 0.0
        )

        self.mat = self.pos_mat @ self.proj_mat

    def update_fovy(self, fovy):
        self.proj_stale = True
        self.fovy = fovy

        ymul = 1.0 / math.tan(fovy / 2)
        xmul = ymul / self.ratio

        self.proj_mat[0,0] = -xmul
        self.proj_mat[1,1] = ymul

        self.mat = self.pos_mat @ self.proj_mat
    