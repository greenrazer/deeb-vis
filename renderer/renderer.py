import math
import random

import moderngl
import moderngl_window
from moderngl_window.conf import settings
from moderngl_window.timers.clock import Timer


class Renderer:
    """
    Custom setup using a class.
    We create the window, main loop and register events.
    """
    def __init__(self, byte_array):
        # Configure to use pyglet window
        settings.WINDOW['class'] = 'moderngl_window.context.pyglet.Window'
        settings.WINDOW['size'] = (720,720)
        settings.WINDOW['aspect_ratio'] = 1

        self.wnd = moderngl_window.create_window_from_settings()

        self.ctx = self.wnd.ctx
        self.ctx.enable(moderngl.DEPTH_TEST)

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

        with open("shaders/tri_vert_shader.glsl") as f:
            vertex_shader = f.read()

        with open("shaders/tri_frag_shader.glsl") as f:
            fragment_shader = f.read()

        self.prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )

        self.prog['z_near'].value = 0.1
        self.prog['z_far'].value = 1000.0
        self.prog['ratio'].value = 1
        self.prog['fovy'].value = 60

        self.prog['eye'].value = (3, 3, 3)
        self.prog['center'].value = (0, 0, 0)
        self.prog['up'].value = (0, 0, 1)

        self.prog['time'].value = 0

        self.shader_args = ("3f4 3f4 3f4 3f4 2f4 3f4 3f4 1f4 3f4 u1 /v", "from_vert", "to_vert", "tangent_translate_from", "tangent_translate_to", "hold_transform_time", "normal", "light_direction", "width_scale", "in_color", "type")

        self.vbo = self.ctx.buffer(byte_array)
        self.vao = self.ctx.vertex_array(self.prog,     [
            (self.vbo, *self.shader_args),
        ])

    def render(self, time, frame_time):
        self.prog['time'].value = time

        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render(moderngl.TRIANGLES)

    def run(self, change_vertex_buffer = None, before_frame_func = None, after_frame_func = None):
        timer = Timer()
        timer.start()

        while not self.wnd.is_closing:
            self.wnd.clear()
            time, frame_time = timer.next_frame()

            if change_vertex_buffer:
                buffer = change_vertex_buffer(self, time, frame_time)
                self.vbo.write(buffer)

            if before_frame_func:
                before_frame_func(self, time, frame_time)

            self.render(time, frame_time)

            if after_frame_func:
                after_frame_func(self, time, frame_time)

            self.wnd.swap_buffers()

        self.wnd.destroy()

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))

    def iconify(self, iconify: bool):
        """Window hide/minimize and restore"""
        print("Window was iconified:", iconify)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        # Key presses
        if action == keys.ACTION_PRESS:
            if key == keys.SPACE:
                print("SPACE key was pressed")

            # Using modifiers (shift and ctrl)

            if key == keys.Z and modifiers.shift:
                print("Shift + Z was pressed")

            if key == keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == keys.SPACE:
                print("SPACE key was released")

        # Move the window around with AWSD
        if action == keys.ACTION_PRESS:
            if key == keys.A:
                self.wnd.position = self.wnd.position[0] - 10, self.wnd.position[1]
            if key == keys.D:
                self.wnd.position = self.wnd.position[0] + 10, self.wnd.position[1]
            if key == keys.W:
                self.wnd.position = self.wnd.position[0], self.wnd.position[1] - 10
            if key == keys.S:
                self.wnd.position = self.wnd.position[0], self.wnd.position[1] + 10

            # toggle cursor
            if key == keys.C:
                self.wnd.cursor = not self.wnd.cursor

            # Shuffle window tittle
            if key == keys.T:
                title = list(self.wnd.title)
                random.shuffle(title)
                self.wnd.title = ''.join(title)

            # Toggle mouse exclusivity
            if key == keys.M:
                self.wnd.mouse_exclusivity = not self.wnd.mouse_exclusivity

    def mouse_position_event(self, x, y, dx, dy):
        print("Mouse position pos={} {} delta={} {}".format(x, y, dx, dy))

    def mouse_drag_event(self, x, y, dx, dy):
        print("Mouse drag pos={} {} delta={} {}".format(x, y, dx, dy))

    def mouse_scroll_event(self, x_offset, y_offset):
        print("mouse_scroll_event", x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))
        print("Mouse states:", self.wnd.mouse_states)

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))
        print("Mouse states:", self.wnd.mouse_states)

    def unicode_char_entered(self, char):
        print("unicode_char_entered:", char)

    def close(self):
        print("Window was closed")
    
