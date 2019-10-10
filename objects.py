import maya.cmds as cmds
import maya.OpenMaya as om


class CharacterModel:
    def __init__(self):
        self.secHeight = 50
        self.neckLenght = 0.5 * (self.secHeight/3.0)
        self.sWidthHalf = self.secHeight/3.0

    def make(self):
        hipCenter = AssignDataPoints().convertToData(xpos=0, ypos=self.secHeight + (self.secHeight/10.0), zpos=0.0, parent=None)
        spine = AssignDataPoints().convertToData(xpos=0, ypos=self.secHeight + (self.secHeight/2.0), zpos=0.0, parent=hipCenter["joint"])
        neckBase = AssignDataPoints().convertToData(xpos=0, ypos=self.secHeight*2.0, zpos=0.0, parent=spine["joint"])

        shoulderBladeLeft = AssignDataPoints().convertToData(xpos=self.sWidthHalf/2.0, ypos=self.secHeight*2.0 - (self.secHeight/12.0), zpos=0.0, parent=neckBase["joint"])
        shoulderLeft = AssignDataPoints().convertToData(xpos=self.sWidthHalf, ypos=self.secHeight*2.0, zpos=0.0, parent=shoulderBladeLeft["joint"])
        elbowLeft = AssignDataPoints().convertToData(self.sWidthHalf + (self.secHeight/2.0), self.secHeight*2.0, 0.0, shoulderLeft["joint"])
        wristLeft = AssignDataPoints().convertToData(self.sWidthHalf + self.secHeight, self.secHeight*2.0, 0.0, elbowLeft["joint"])
        handLeft = AssignDataPoints().convertToData(self.sWidthHalf + self.secHeight + (self.secHeight/12.0), self.secHeight*2.0, 0.0, wristLeft["joint"])

        shoulderBladeRight = AssignDataPoints().convertToData(-self.sWidthHalf/2.0, self.secHeight*2.0 - (self.secHeight/12.0), 0.0, neckBase["joint"])
        shoulderRight = AssignDataPoints().convertToData(-self.sWidthHalf, self.secHeight*2.0, 0.0, shoulderBladeRight["joint"])
        elbowRight = AssignDataPoints().convertToData(-self.sWidthHalf - (self.secHeight/2.0), self.secHeight*2.0, 0.0, shoulderRight["joint"])
        wristRight = AssignDataPoints().convertToData(-self.sWidthHalf - self.secHeight, self.secHeight*2.0, 0.0, elbowRight["joint"])
        handRight = AssignDataPoints().convertToData(-self.sWidthHalf - self.secHeight - (self.secHeight/12.0), self.secHeight*2.0, 0.0, wristRight["joint"])

        hipLeft = AssignDataPoints().convertToData(self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0.0, hipCenter["joint"])
        kneeLeft = AssignDataPoints().convertToData(self.sWidthHalf*0.5, self.secHeight/2.0, 0.0, hipLeft["joint"])
        ankleLeft = AssignDataPoints().convertToData(self.sWidthHalf*0.5, 0.0, 0.0, kneeLeft["joint"])
        footLeft = AssignDataPoints().convertToData(self.sWidthHalf*0.5, 0.0, self.sWidthHalf*0.75, ankleLeft["joint"])

        hipRight = AssignDataPoints().convertToData(-self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0.0, hipCenter["joint"])
        kneeRight = AssignDataPoints().convertToData(-self.sWidthHalf*0.5, self.secHeight/2.0, 0.0, hipRight["joint"])
        ankleRight = AssignDataPoints().convertToData(-self.sWidthHalf*0.5, 0.0, 0.0, kneeRight["joint"])
        footRight = AssignDataPoints().convertToData(-self.sWidthHalf*0.5, 0.0, self.sWidthHalf*0.75, ankleRight["joint"])

        return hipCenter, spine, neckBase, shoulderBladeLeft, shoulderLeft, elbowLeft, wristLeft, handLeft, \
               shoulderBladeRight, shoulderRight, elbowRight, wristRight, handRight, hipLeft, kneeLeft, ankleLeft, \
               footLeft, hipRight, kneeRight, ankleRight, footRight


class AssignDataPoints:
    def convertToData(self, xpos, ypos, zpos, parent):
        cmds.select(clear=True)
        joint = cmds.joint(p=(xpos, ypos, zpos))
        return {"joint":joint, "parent":parent, "rotateX":0.0, "rotateY":0.0, "rotateZ":0.0,
                "posX":xpos, "posY":ypos, "posZ":zpos}
