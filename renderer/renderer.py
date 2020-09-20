from utils.timer import Timer

class Renderer:
    def __init__(self):
        self.before_render_funcs = []
        self.after_render_funcs = []
        self.advance_time_func = None
        self.vertex_array_objects = []

    def add_before_render_function(self, func):
        self.before_render_funcs.append(func)

    def add_after_render_function(self, func):
        self.after_render_funcs.append(func)

    def set_advance_time_function(self, func):
        self.advance_time_func = func

    @property
    def stopping_condition(self):
        raise NotImplementedError("No stopping condition on Renderer: maybe you need to instansiate a subclass.")

    def on_destroy(self, current_time, total_time, frames):
        raise NotImplementedError("No destory method on Renderer: maybe you need to instansiate a subclass.")

    def render(self):
        raise NotImplementedError("No render method on Renderer: maybe you need to instansiate a subclass.")

    def run(self):
        timer = Timer()
        timer.start()
        frames = 0

        while self.stopping_condition:
            time, frame_time = timer.next_frame()
            frames += 1

            if self.before_render_funcs:
                for func in self.before_render_funcs:
                    func(self, time, frame_time)

            if self.advance_time_func:
                self.advance_time_func(self, time, frame_time)

            self.render()

            if self.after_render_funcs:
                for func in self.after_render_funcs:
                    func(self, time, frame_time)

        current_time, total_time = timer.stop()
        self.on_destroy(current_time, total_time, frames)

    
    def add_vertex_array_object(self, vao):
        self.vertex_array_objects.append(vao)
