from scene.objects.sceneobject import SceneObject

class TransformableSceneObject(SceneObject):
    def __init__(self):
        SceneObject.__init__(self)
        self.animated = True