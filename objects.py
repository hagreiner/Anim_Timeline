import maya.cmds as cmds
import maya.OpenMaya as om


class CharacterModel:
    def __init__(self):
        self.secHeight = 50
        self.neckLenght = 0.5 * (self.secHeight/3.0)
        self.sWidthHalf = self.secHeight/3.0

    def make(self):
        pass


class AssignDataPoints:
    def convertToData(self, xpos, ypos, zpos, parent):
        cmds.select(clear=True)
        joint = cmds.joint(p=(xpos, ypos, zpos))
        return {"joint":joint, "parent":parent, "rotateX":0.0, "rotateY":0.0, "rotateZ":0.0,
                "posX":xpos, "posY":ypos, "posZ":zpos}
