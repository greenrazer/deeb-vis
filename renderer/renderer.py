import moderngl

from utils.timer import Timer

class Renderer:
    def __init__(self):
        self.before_render_funcs = []
        self.after_render_funcs = []
        self.advance_time_func = None
        self.render_trees = []

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

    def immediate_before_render(self):
        raise NotImplementedError()

    def immediate_after_render(self):
        raise NotImplementedError()

    def render(self):
        self.immediate_before_render()
        for tree in self.render_trees:
            tree.render()
        self.immediate_after_render()

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

    
    def add_render_tree_obj(self, tree):
        self.render_trees.append(tree)
