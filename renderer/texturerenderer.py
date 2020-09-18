import moderngl

from base.renderer.renderer import Renderer

class TextureRenderer(Renderer):
    def __init__(self, size=(256, 256), components=4, samples=4):
        Renderer.__init__(self)
        self.ctx = moderngl.create_standalone_context(require=430)
        self.texture = self.ctx.texture(size, components=4)
        self.fbo1 = self.ctx.simple_framebuffer(size, samples=samples)
        self.fbo2 = self.ctx.framebuffer(self.texture)
        self.scope = self.ctx.scope(self.fbo1)

    def __enter__(self):
        self.scope.__enter__()

    def __exit__(self, *args):
        self.scope.__exit__()
        self.ctx.copy_framebuffer(self.fbo2, self.fbo1)

    def render(self, time, frame_time):
        self.texture = self.texture1
        self.fbo.clear(1.0, 1.0, 1.0)
        self.fbo.use()