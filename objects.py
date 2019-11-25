import maya.cmds as cmds
import maya.OpenMaya as om


class CharacterModel:
    def __init__(self):
        self.legthUnit = -10
        self.jointNumber = 5
        self.jointList = []

    def makeRig(self):
        for x in range(self.jointNumber):
            joint = cmds.joint(p=(0, 0, self.legthUnit*x))
            self.jointList.append(joint)

        handle_1 = createHandle(self.jointList[0], self.jointList[2])
        handle_2 = createHandle(self.jointList[2], self.jointList[4])

        cmds.rotate(0, 0, -90, self.jointList[0])

        return handle_1, handle_2

    def mesh(self):
        item = cmds.polyPlane(w=10, h=abs(self.legthUnit)*self.jointNumber)
        cmds.move(0, 0, self.legthUnit*self.jointNumber/2.0 - self.legthUnit/2.0, item)
        return item


class AssignDataPoints:
    def convertToData(self, xpos, ypos, zpos, parent):
        cmds.select(clear=True)
        joint = cmds.joint(p=(xpos, ypos, zpos))
        return {"joint":joint, "parent":parent, "rotateX":0.0, "rotateY":0.0, "rotateZ":0.0,
                "posX":xpos, "posY":ypos, "posZ":zpos}


def createHandle(start, end):
    handle = cmds.ikHandle(sj=start, ee=end)
    return handle