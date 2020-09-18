from scene.objects.sceneobject import SceneObject
from scene.objects.transformablesceneobject import TransformableSceneObject

from scene.cameras.camera import Camera

from renderer.renderer import Renderer

from shaders.shadercompiler import ShaderCompiler

class Scene:
    def __init__(self, camera, compiler, renderer):
        if not isinstance(compiler, ShaderCompiler):
            raise TypeError(f"{compiler.__class__.__name__} is not a ShaderCompiler.")

        if not isinstance(renderer, Renderer):
            raise TypeError(f"{renderer.__class__.__name__} is not a Renderer.")

        if not isinstance(camera, Camera):
            raise TypeError(f"{camera.__class__.__name__} is not a Camera.")

        self.camera = camera
        self.compiler = compiler
        self.renderer = renderer
        self.compiled = False
        self.time_increment = 1

        self.renderer.add_before_render_function(self.check_camera_change)
        # self.renderer.set_advance_time_function(self.advance_time)

        self.static_scene_objs = []
        self.transformable_scene_objs = []

    def check_camera_change(self, renderer, time, frame_time):
        if self.camera.pos_stale:
            self.program['camera_pos'].value = self.camera.position.to_tuple()
            self.camera.pos_stale = False
        if self.camera.proj_stale:
            self.program['projection_matrix'].value = self.camera.projection.to_tuple()
            self.camera.proj_stale = False

    def advance_time(self, renderer, time, frame_time):
        if abs(frame_time) > 1500000:
            return
        import math
        self.program['time'].value = 4*math.sin(0.7*time)
        # self.program['time'].value += frame_time*self.time_increment

    def add_transformable_object(self, obj):
        self.compiled = False
        if not isinstance(obj, TransformableSceneObject):
            raise TypeError(f"{obj.__class__.__name__} is not transformable.")
        self.transformable_scene_objs.append(obj)

    def add_static_object(self, obj):
        self.compiled = False
        if not isinstance(obj, SceneObject):
            raise TypeError(f"{obj.__class__.__name__} cannot be added to the scene.")
        self.static_scene_objs.append(obj)

    def attach_uniforms(self):
        self.program['camera_pos'].value = self.camera.position.to_tuple()
        self.program['projection_matrix'].value = self.camera.projection.to_tuple()

    def compile(self):
        self.compiled = True
        self.program = self.compiler.compile(self.renderer.context)
        self.attach_uniforms()
        self.renderer.set_program(self.program)
        self.renderer.set_vertex_buffer(self.to_bytes())

    def run(self):
        if not self.compiled:
            raise RuntimeError("Must compile shaders before running program.")
        self.renderer.run()
    
    @property
    def num_verts(self):
        verts = 0
        for s in self.static_scene_objs:
            verts += s.num_verts
        for t in self.transformable_scene_objs:
            verts += t.num_verts
        return verts

    def to_bytes(self):
        buf = bytearray(self.num_verts*SceneObject.bytes_per_vertex)
        at = 0
        for s in self.static_scene_objs:
            to_write = s.to_bytes()
            buf[at:at+len(to_write)] = to_write
            at += len(to_write)
        
        for t in self.transformable_scene_objs:
            to_write = t.to_bytes()
            buf[at:at+len(to_write)] = to_write
            at += len(to_write)
        return buf
