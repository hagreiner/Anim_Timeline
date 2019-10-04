import maya.cmds as cmds

class CharacterModel:
    def __init__(self):
        self.secHeight = 50
        self.neckLenght = 0.5 * (self.secHeight/3.0)
        self.sWidthHalf = self.secHeight/3.0

    def make(self):
        # hipCenter = cmds.joint(p=(0, self.secHeight + (self.secHeight/10.0), 0))
        # cmds.select(clear=True)
        # spine = cmds.joint(p=(0, self.secHeight + (self.secHeight/2.0), 0))
        # cmds.select(clear=True)
        # neckBase = cmds.joint(p=(0, self.secHeight*2.0, 0))
        #
        # cmds.select(clear=True)
        # shoulderBladeLeft = cmds.joint(p=(self.sWidthHalf/2.0, self.secHeight*2.0 - (self.secHeight/12.0), 0))
        # cmds.select(clear=True)
        # shoulderLeft = cmds.joint(p=(self.sWidthHalf, self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        # elbowLeft = cmds.joint(p=(self.sWidthHalf + (self.secHeight/2.0), self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        # wristLeft = cmds.joint(p=(self.sWidthHalf + self.secHeight, self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        # handLeft = cmds.joint(p=(self.sWidthHalf + self.secHeight + (self.secHeight/12.0), self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        #
        # cmds.select(clear=True)
        # shoulderBladeRight = cmds.joint(p=(-self.sWidthHalf/2.0, self.secHeight*2.0 - (self.secHeight/12.0), 0))
        # cmds.select(clear=True)
        # shoulderRight = cmds.joint(p=(-self.sWidthHalf, self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        # elbowRight = cmds.joint(p=(-self.sWidthHalf - (self.secHeight/2.0), self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        # wristRight = cmds.joint(p=(-self.sWidthHalf - self.secHeight, self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        # handRight = cmds.joint(p=(-self.sWidthHalf - self.secHeight - (self.secHeight/12.0), self.secHeight*2.0, 0))
        # cmds.select(clear=True)
        #
        # cmds.select(clear=True)
        # hipLeft = cmds.joint(p=(self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0))
        # cmds.select(clear=True)
        # kneeLeft = cmds.joint(p=(self.sWidthHalf*0.5, self.secHeight/2.0, 0))
        # cmds.select(clear=True)
        # ankleLeft = cmds.joint(p=(self.sWidthHalf*0.5, 0, 0))
        # cmds.select(clear=True)
        # footLeft = cmds.joint(p=(self.sWidthHalf*0.5, 0, self.sWidthHalf*0.75))
        #
        # cmds.select(clear=True)
        # hipRight = cmds.joint(p=(-self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0))
        # cmds.select(clear=True)
        # kneeRight = cmds.joint(p=(-self.sWidthHalf*0.5, self.secHeight/2.0, 0))
        # cmds.select(clear=True)
        # ankleRight = cmds.joint(p=(-self.sWidthHalf*0.5, 0, 0))
        # cmds.select(clear=True)
        # footRight = cmds.joint(p=(-self.sWidthHalf*0.5, 0, self.sWidthHalf*0.75))
        # cmds.select(clear=True)

        hipCenter = AssignDataPoints().convertToData(xpos=0, ypos=self.secHeight + (self.secHeight/10.0), zpos=0, parent=None)
        spine = AssignDataPoints().convertToData(xpos=0, ypos=self.secHeight + (self.secHeight/2.0), zpos=0, parent=hipCenter["joint"])
        neckBase = AssignDataPoints().convertToData(xpos=0, ypos=self.secHeight*2.0, zpos=0, parent=spine["joint"])

        shoulderBladeLeft = AssignDataPoints().convertToData(xpos=self.sWidthHalf/2.0, ypos=self.secHeight*2.0 - (self.secHeight/12.0), zpos=0, parent=neckBase["joint"])
        shoulderLeft = AssignDataPoints().convertToData(xpos=self.sWidthHalf, ypos=self.secHeight*2.0, zpos=0, parent=shoulderBladeLeft["joint"])
        elbowLeft = AssignDataPoints().convertToData(self.sWidthHalf + (self.secHeight/2.0), self.secHeight*2.0, 0, shoulderLeft["joint"])
        wristLeft = AssignDataPoints().convertToData(self.sWidthHalf + self.secHeight, self.secHeight*2.0, 0, elbowLeft["joint"])
        handLeft = AssignDataPoints().convertToData(self.sWidthHalf + self.secHeight + (self.secHeight/12.0), self.secHeight*2.0, 0, wristLeft["joint"])

        shoulderBladeRight = cmds.joint(p=(-self.sWidthHalf/2.0, self.secHeight*2.0 - (self.secHeight/12.0), 0))
        cmds.select(clear=True)
        shoulderRight = cmds.joint(p=(-self.sWidthHalf, self.secHeight*2.0, 0))
        cmds.select(clear=True)
        elbowRight = cmds.joint(p=(-self.sWidthHalf - (self.secHeight/2.0), self.secHeight*2.0, 0))
        cmds.select(clear=True)
        wristRight = cmds.joint(p=(-self.sWidthHalf - self.secHeight, self.secHeight*2.0, 0))
        cmds.select(clear=True)
        handRight = cmds.joint(p=(-self.sWidthHalf - self.secHeight - (self.secHeight/12.0), self.secHeight*2.0, 0))
        cmds.select(clear=True)

        cmds.select(clear=True)
        hipLeft = cmds.joint(p=(self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0))
        cmds.select(clear=True)
        kneeLeft = cmds.joint(p=(self.sWidthHalf*0.5, self.secHeight/2.0, 0))
        cmds.select(clear=True)
        ankleLeft = cmds.joint(p=(self.sWidthHalf*0.5, 0, 0))
        cmds.select(clear=True)
        footLeft = cmds.joint(p=(self.sWidthHalf*0.5, 0, self.sWidthHalf*0.75))

        cmds.select(clear=True)
        hipRight = cmds.joint(p=(-self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0))
        cmds.select(clear=True)
        kneeRight = cmds.joint(p=(-self.sWidthHalf*0.5, self.secHeight/2.0, 0))
        cmds.select(clear=True)
        ankleRight = cmds.joint(p=(-self.sWidthHalf*0.5, 0, 0))
        cmds.select(clear=True)
        footRight = cmds.joint(p=(-self.sWidthHalf*0.5, 0, self.sWidthHalf*0.75))
        cmds.select(clear=True)

        return hipCenter, spine, neckBase, shoulderBladeLeft, shoulderLeft, elbowLeft, wristLeft, handLeft, \
               shoulderBladeRight, shoulderRight, elbowRight, wristRight, handRight, hipLeft, kneeLeft, ankleLeft, \
               footLeft, hipRight, kneeRight, ankleRight, footRight


class AssignDataPoints:
    def convertToData(self, xpos, ypos, zpos, parent):
        cmds.select(clear=True)
        joint = cmds.joint(p=(xpos, ypos, zpos))
        return {"joint":joint, "parent":parent, "rotateX":0, "rotateY":0, "rotateZ":0,
                "posX":xpos, "posY":ypos, "posZ":zpos}
