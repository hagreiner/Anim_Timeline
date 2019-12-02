import maya.cmds as cmds
import maya.OpenMaya as om


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

        handle_1 = createHandle(self.jointList[0], self.jointList[2], name="closeHandle")
        handle_2 = createHandle(self.jointList[2], self.jointList[4], name="farHandle")

        # cmds.rotate(0, 0, -90, self.jointList[0])

        close = createNurbsHandle(self.legthUnit*2, "closeHandle")
        far = createNurbsHandle(self.legthUnit*4, "farHandle")

        return self.jointList[0], close, far

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


def createHandle(start, end, name):
    handle = cmds.ikHandle(sj=start, ee=end, pcv=True, p=1, n=name)
    return handle

def createNurbsHandle(location, ik):
    cmds.spaceLocator(n='ik_loc_' + ik)
    pelvisPos = cmds.xform(ik, q=True, ws=True, t=True)
    cmds.xform('ik_loc_' + ik, ws=True, t=pelvisPos)
    cmds.poleVectorConstraint('ik_loc_' + ik, ik, weight=1)

    circle = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=5)
    cmds.move(0, 0, location, circle, relative=True)

    cmds.parentConstraint(circle, ik, mo=True)

    return circle
    # cmds.pointConstraint(circle, ik)
    # cmds.orientConstraint(circle, ik)
    # point
    # orient