from scene.objects.sceneobject import SceneObject

from scene.cameras.camera import Camera

from renderer.renderer import Renderer

from renderer.screenrenderunit import ScreenRenderUnit
from renderer.texturerenderunit import TextureRenderUnit

from shaders.bufferbuilders.spherebufferbuilder import SphereBufferBuilder
from shaders.bufferbuilders.staticlinebufferbuilder import StaticLineBufferBuilder
from shaders.bufferbuilders.translinebufferbuilder import TransLineBufferBuilder
from shaders.bufferbuilders.screenbufferbuilder import ScreenBufferBuilder

class Scene:
    buffer_builder_classes = (
        SphereBufferBuilder,
        StaticLineBufferBuilder,
        TransLineBufferBuilder,
        ScreenBufferBuilder
    )

    def __init__(self, camera, renderer, size = None, subscene = False):

        if not isinstance(renderer, Renderer):
            raise TypeError(f"{renderer.__class__.__name__} is not a Renderer.")

        if not isinstance(camera, Camera):
            raise TypeError(f"{camera.__class__.__name__} is not a Camera.")
        
        self.subscene = subscene
        self.subscenes = []
        self.size = size if size else renderer.size

        self.tree = None

        self.camera = camera
        self.renderer = renderer
        self.compiled = False
        self.time_increment = 1

        self.renderer.add_before_render_function(self.check_camera_change)
        # self.renderer.set_advance_time_function(self.advance_time)

        self.scene_objs = []

    def check_camera_change(self, renderer, time, frame_time):
            if self.compiled:
                if self.camera.pos_stale:
                    self.set_uniform_for_all('camera_pos', self.camera.position.to_tuple())
                    self.camera.pos_stale = False
                if self.camera.proj_stale:
                    self.set_uniform_for_all('projection_matrix', self.camera.projection.to_tuple())
                    self.camera.proj_stale = False

    def advance_time(self, renderer, time, frame_time):
        if abs(frame_time) > 1500000:
            return
        import math
        self.set_uniform_for_all('time', 4*math.sin(0.7*time))

    def add_scene_object(self, obj):
        self.compiled = False
        if not isinstance(obj, SceneObject):
            raise TypeError(f"{obj.__class__.__name__} cannot be added to the scene.")
        self.scene_objs.append(obj)

    def set_uniform_for_all(self, name, value):
        for b in self.buffer_builders:
            b.set_uniform(name, value)


    def attach_uniforms(self):
        self.set_uniform_for_all('camera_pos', self.camera.position.to_tuple())
        self.set_uniform_for_all('projection_matrix', self.camera.projection.to_tuple())
        self.set_uniform_for_all('time', 0)
        self.set_uniform_for_all('light_direction', (0.0,0.0,1.0))

    def generate_buffer_builders(self):
        raise NotImplementedError()

    def compile(self):
        self.compiled = True
        
        self.buffer_builders = self.generate_buffer_builders()
        
        vaos = []
        for b in self.buffer_builders:
            vao = b.build(self.renderer.context)
            vaos.append(vao)

        if self.subscene:
            self.tree = TextureRenderUnit(self.renderer.context, vaos, self.size)
        else:
            self.tree = ScreenRenderUnit(self.renderer.context, vaos)

        self.attach_uniforms() 

        for sub in self.subscenes:
            sub.compile()
            self.tree.add_child(sub.tree)

    def attach_sub_scene(self, subscene):
        subscene.subscene = True
        self.subscenes.append(subscene)

    def run(self):
        if not self.compiled:
            raise RuntimeError("Must compile shaders before running program.")
        self.renderer.add_render_tree_obj(self.tree)
        self.renderer.run()
