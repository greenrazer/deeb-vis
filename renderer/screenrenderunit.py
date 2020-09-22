import moderngl

from renderer.renderunit import RenderUnit

class ScreenRenderUnit(RenderUnit):
    def __init__(self, context, vaos):
        RenderUnit.__init__(self)

        self.context = context

        self.vaos = vaos
        self.render_mode = moderngl.TRIANGLES
        
    def render_unit(self):
        self.context.screen.use()
        self.context.clear(1.0, 1.0, 1.0)
        for v in self.vaos:
            v.render(self.render_mode)
        return None