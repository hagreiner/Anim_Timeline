import maya.cmds as cmds
import maya.OpenMaya as om
import math
import ikCreation


class CharacterModel:
    def __init__(self):
        self.legthUnit = -10
        self.jointNumber = 5
        self.jointList = []

    def makeRig(self):
        cmds.select(clear=True)
        for x in range(self.jointNumber):
            joint = cmds.joint(p=(0, 0, self.legthUnit*x))
            self.jointList.append(joint)

        handle_1 = ikCreation.createHandle(self.jointList[0], self.jointList[2], name="closeHandle")
        handle_2 = ikCreation.createHandle(self.jointList[2], self.jointList[4], name="farHandle")

        # (nurbsLocationList, nurbsSize, nurbsRotation, ik, addedLocatorList)
        close = ikCreation.createNurbsHandle([0, 0, self.legthUnit*2], [5, 5, 5], [0, 0, 0], "closeHandle", [0, 0, 0], False)
        far = ikCreation.createNurbsHandle([0, 0, self.legthUnit*4], [5, 5, 5], [0, 0, 0], "farHandle", [0, 0, 0], False)

        return self.jointList[0], close, far

    def mesh(self):
        item = cmds.polyCylinder(r=2.5, h=abs(self.legthUnit)*self.jointNumber, sy=10)
        cmds.move(0, 0, self.legthUnit*self.jointNumber/2.0 - self.legthUnit/2.0, item)
        cmds.rotate(90, 0, 0, item)
        return item


class AssignDataPoints:
    def convertToData(self, xpos, ypos, zpos, parent):
        cmds.select(clear=True)
        joint = cmds.joint(p=(xpos, ypos, zpos))
        return {"joint":joint, "parent":parent, "rotateX":0.0, "rotateY":0.0, "rotateZ":0.0,
                "posX":xpos, "posY":ypos, "posZ":zpos}