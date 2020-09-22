class RenderUnit:
    def __init__(self):
        self.children = []

    def add_child(self, ru):
        if not isinstance(ru, RenderUnit):
            raise RuntimeError("not a render unit")
        self.children.append(ru)

    def render_children(self):
        for location, child in enumerate(self.children):
            child.render().use(location=location)
    
    def render_unit(self):
        pass

    def render(self):
        self.render_children()
        return self.render_unit()

    def visit(self, func):
        func(self)
        for child in self.children:
            child.visit(func)
        


    