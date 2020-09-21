import moderngl

from base.renderer.renderer import Renderer

class TextureRenderer(Renderer):
    def __init__(self, size=(256, 256), components=4, samples=4):
        Renderer.__init__(self)
        self.ctx = moderngl.create_standalone_context(require=430)
        self.texture = self.ctx.texture(size, components=4)
        depth_attachment = self.ctx.depth_renderbuffer(size)
        self.fbo = self.ctx.framebuffer(self.texture, depth_attachment)

    @property
    def stopping_condition(self):
        pass

    def on_destroy(self, current_time, total_time, frames):
        pass

    def immediate_before_render(self):
        self.fbo.clear(1.0, 1.0, 1.0)

    def render_vao(self, vao, render_mode = moderngl.TRIANGLES):
        self.fbo.use()
        vao.render(render_mode)

    def immediate_after_render(self):
        pass