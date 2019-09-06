"""
defaultNavigation -createNew -destination "Animated_PBR.color";
createRenderNode -allWithTexturesUp "defaultNavigation -force true -connectToExisting -source %node -destination Animated_PBR.color" "";
defaultNavigation -defaultTraversal -destination "Animated_PBR.color";

"""
import maya.cmds as cmds
from constants import SHADER_NAME


class CreateShader:
    def create(self):
        cmds.shadingNode('StingrayPBS', asShader=True, name=SHADER_NAME)


class AssignShader:
    def __init__(self, object):
        self.object = object

    def add(self):
        cmds.sets(name="MAT_GROUP", renderable=True, empty=True)
        cmds.surfaceShaderList(SHADER_NAME, add="MAT_GROUP")
        cmds.sets(self.object, e=True, forceElement="MAT_GROUP")