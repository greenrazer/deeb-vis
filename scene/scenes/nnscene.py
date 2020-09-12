from scene.scenes.scene import Scene

from scene.objects.sceneobject import SceneObject
from scene.objects.transformablesceneobject import TransformableSceneObject

from scene.cameras.camera import Camera

from renderer.renderer import Renderer

from shaders.nncompiler import NNCompiler

class NNScene(Scene):
    def __init__(self, camera, renderer): 
        self.curr_timing = 0
        self.steps = []
        Scene.__init__(self, 
            compiler = NNCompiler(self.steps), 
            camera = camera, 
            renderer = renderer)

    def add_mba_step_transformation(self, matrix, bias, activation, m_timing, b_timing, a_timing):
        m_time = (self.curr_timing + m_timing[0], self.curr_timing + m_timing[1])
        b_time = (m_time[1] + b_timing[0], m_time[1] + b_timing[1])
        a_time = (b_time[1] + a_timing[0], b_time[1] + a_timing[1])
        self.curr_timing = a_time[1]

        self.steps.append({
            'matrix': matrix, 
            'bias': bias, 
            'activation': activation, 
            'm_time': m_time, 
            'b_time': b_time, 
            'a_time': a_time
        })

    def add_transformations_to_uniforms(self):
        if not self.compiled:
            raise RuntimeError("Must compile shaders before attaching transformations to uniforms")
        for i in range(len(self.steps)):
            self.program[self.compiler.uniforms[i][0]].value = self.steps[i]['matrix'].to_tuple()
            self.program[self.compiler.uniforms[i][1]].value = self.steps[i]['bias'].to_tuple()
            self.program[self.compiler.uniforms[i][2]].value = self.steps[i]['m_time']
            self.program[self.compiler.uniforms[i][3]].value = self.steps[i]['b_time']
            self.program[self.compiler.uniforms[i][4]].value = self.steps[i]['a_time']

    def compile(self):
        Scene.compile(self)
        self.add_transformations_to_uniforms()
