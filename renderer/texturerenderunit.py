import moderngl

from renderer.renderunit import RenderUnit

class TextureRenderUnit(RenderUnit):
    def __init__(self, context, vaos, size, components=4):
        RenderUnit.__init__(self)

        self.texture = context.texture(size, components=4)
        depth_attachment = context.depth_renderbuffer(size)
        self.fbo = context.framebuffer(self.texture, depth_attachment)

        self.vaos = vaos
        self.render_mode = moderngl.TRIANGLES
        
    def render_unit(self):
        self.fbo.clear(1.0, 1.0, 1.0)
        self.fbo.use()
        for v in self.vaos:
            v.render(self.render_mode)
        return self.texture