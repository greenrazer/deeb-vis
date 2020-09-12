import math
import random

import moderngl
import moderngl_window
from moderngl_window.conf import settings
from moderngl_window.timers.clock import Timer

from base.matrix4 import Matrix4
from base.matrix3 import Matrix3
from base.vector3 import Vector3

from renderer.renderer import Renderer

DEFAULT_WINDOW_SETTINGS = {
    'class': 'moderngl_window.context.pyglet.Window',
    'size': (720, 720),
    'aspect_ratio': 1
}

DEFAULT_CONTEXT_ENABLES = moderngl.DEPTH_TEST

DEFAULT_RENDERER_SETTINGS = {
    'clear_color': (1.0, 1.0, 1.0)
}

class WindowRenderer(Renderer):
    def __init__(self, 
                window_settings = DEFAULT_WINDOW_SETTINGS, 
                context_enables = DEFAULT_CONTEXT_ENABLES,
                renderer_settings = DEFAULT_RENDERER_SETTINGS):

        Renderer.__init__(self)

        for key, value in window_settings.items():
            settings.WINDOW[key] = value

        for key, value in renderer_settings.items():
            setattr(self, key, value)

        self.wnd = moderngl_window.create_window_from_settings()

        self.context = self.wnd.ctx
        self.context.enable(context_enables)

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

    def set_clear_color(self, color):
        self.clear_color = color

    def render(self, time, frame_time):
        self.program['time'].value = time
        self.context.clear(*self.clear_color)
        self.vao.render(moderngl.TRIANGLES)

    def run(self):
        timer = Timer()
        timer.start()

        while not self.wnd.is_closing:
            self.wnd.clear()
            time, frame_time = timer.next_frame()

            if self.before_render_funcs:
                for func in self.before_render_funcs:
                    func(self, time, frame_time)

            self.render(time, frame_time)

            if self.after_render_funcs:
                for func in self.after_render_funcs:
                    func(self, time, frame_time)

            self.wnd.swap_buffers()

        self.wnd.destroy()

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