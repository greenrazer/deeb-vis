import math
import random

import moderngl
import moderngl_window
from moderngl_window.conf import settings
from moderngl_window.utils.module_loading import import_string

from base.matrix4 import Matrix4
from base.matrix3 import Matrix3
from base.vector3 import Vector3

from renderer.renderer import Renderer

DEFAULT_WINDOW_SETTINGS = {
    'class': 'moderngl_window.context.pyglet.Window',
    'size': (720, 720),
    'aspect_ratio': 1,
    "gl_version": (4, 3)
}

DEFAULT_CONTEXT_ENABLES = moderngl.DEPTH_TEST

DEFAULT_RENDERER_SETTINGS = {
    'clear_color': (1.0, 1.0, 1.0)
}

class WindowRenderer(Renderer):
    def __init__(self, 
                context = None,
                window_settings = DEFAULT_WINDOW_SETTINGS, 
                context_enables = DEFAULT_CONTEXT_ENABLES,
                renderer_settings = DEFAULT_RENDERER_SETTINGS):

        Renderer.__init__(self)

        for key, value in renderer_settings.items():
            setattr(self, key, value)

        self.context = context if context else moderngl.create_standalone_context(require=430)
        window_cls = import_string(window_settings["class"])
        self.wnd = window_cls(**window_settings)
        self.context.enable(context_enables)
        moderngl_window.activate_context(self.wnd, self.context)

        # register event methods
        self.wnd.resize_func = self.resize
        self.wnd.iconify_func = self.iconify
        self.wnd.key_event_func = self.key_event
        self.wnd.mouse_position_event_func = self.mouse_position_event
        self.wnd.mouse_drag_event_func = self.mouse_drag_event
        self.wnd.mouse_scroll_event_func = self.mouse_scroll_event
        self.wnd.mouse_press_event_func = self.mouse_press_event
        self.wnd.mouse_release_event_func = self.mouse_release_event
        self.wnd.unicode_char_entered_func = self.unicode_char_entered
        self.wnd.close_func = self.close

        self.set_advance_time_function(self.advance_time)

    def set_clear_color(self, color):
        self.clear_color = color

    def render(self):
        self.wnd.clear(*self.clear_color)
        self.context.clear(*self.clear_color)
        self.vao.render(moderngl.TRIANGLES)
        self.wnd.swap_buffers()

    def advance_time(self, renderer, time, frame_time):
        self.program['time'].value = time

    @property
    def stopping_condition(self):
        return not self.wnd.is_closing

    def on_destroy(self,current_time, total_time, frames):
        self.wnd.destroy()
        print(f"Run took :{total_time}s at {frames/total_time}avg fps.")

    def resize(self, width: int, height: int):
        pass

    def iconify(self, iconify):
        pass

    def key_event(self, key, action, modifiers):
        pass

    def mouse_position_event(self, x, y, dx, dy):
        pass

    def mouse_drag_event(self, x, y, dx, dy):
        pass

    def mouse_scroll_event(self, x_offset, y_offset):
        pass

    def mouse_press_event(self, x, y, button):
        pass

    def mouse_release_event(self, x, y, button):
        pass

    def unicode_char_entered(self, char):
        pass

    def close(self):
        pass