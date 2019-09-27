import maya.cmds as cmds

class CharacterModel:
    def __init__(self):
        self.secHeight = 50
        self.neckLenght = 0.5 * (self.secHeight/3.0)
        self.sWidthHalf = self.secHeight/3.0

    def make(self):
        cmds.select(d=True)
        hipCenter = cmds.joint(p=(0, self.secHeight + (self.secHeight/10.0), 0))
        spine = cmds.joint(p=(0, self.secHeight + (self.secHeight/2.0), 0))
        cmds.joint(hipCenter, e=True, zso=True, oj='xyz')
        neckBase = cmds.joint(p=(0, self.secHeight*2.0, 0))
        cmds.joint(spine, e=True, zso=True, oj='xyz')

        shoulderBladeLeft = cmds.joint(p=(self.sWidthHalf/2.0, self.secHeight*2.0 - (self.secHeight/12.0), 0))
        cmds.joint(neckBase, e=True, zso=True, oj='xyz')
        shoulderLeft = cmds.joint(p=(self.sWidthHalf, self.secHeight*2.0, 0))
        cmds.joint(shoulderBladeLeft, e=True, zso=True, oj='xyz')
        elbowLeft = cmds.joint(p=(self.sWidthHalf + (self.secHeight/2.0), self.secHeight*2.0, 0))
        cmds.joint(shoulderLeft, e=True, zso=True, oj='xyz')
        wristLeft = cmds.joint(p=(self.sWidthHalf + self.secHeight, self.secHeight*2.0, 0))
        cmds.joint(elbowLeft, e=True, zso=True, oj='xyz')
        handLeft = cmds.joint(p=(self.sWidthHalf + self.secHeight + (self.secHeight/12.0), self.secHeight*2.0, 0))
        cmds.joint(wristLeft, e=True, zso=True, oj='xyz')

        cmds.select(clear=True)
        cmds.select(neckBase)
        shoulderBladeRight = cmds.joint(p=(-self.sWidthHalf/2.0, self.secHeight*2.0 - (self.secHeight/12.0), 0))
        cmds.joint(neckBase, e=True, zso=True, oj='xyz')
        shoulderRight = cmds.joint(p=(-self.sWidthHalf, self.secHeight*2.0, 0))
        cmds.joint(shoulderBladeRight, e=True, zso=True, oj='xyz')
        elbowRight = cmds.joint(p=(-self.sWidthHalf - (self.secHeight/2.0), self.secHeight*2.0, 0))
        cmds.joint(shoulderRight, e=True, zso=True, oj='xyz')
        wristRight = cmds.joint(p=(-self.sWidthHalf - self.secHeight, self.secHeight*2.0, 0))
        cmds.joint(elbowRight, e=True, zso=True, oj='xyz')
        handRight = cmds.joint(p=(-self.sWidthHalf - self.secHeight - (self.secHeight/12.0), self.secHeight*2.0, 0))
        cmds.joint(wristRight, e=True, zso=True, oj='xyz')

        cmds.select(clear=True)
        cmds.select(hipCenter)
        hipLeft = cmds.joint(p=(self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0))
        cmds.joint(hipCenter, e=True, zso=True, oj='xyz')
        kneeLeft = cmds.joint(p=(self.sWidthHalf*0.5, self.secHeight/2.0, 0))
        cmds.joint(hipLeft, e=True, zso=True, oj='xyz')
        ankleLeft = cmds.joint(p=(self.sWidthHalf*0.5, 0, 0))
        cmds.joint(kneeLeft, e=True, zso=True, oj='xyz')
        footLeft = cmds.joint(p=(self.sWidthHalf*0.5, 0, self.sWidthHalf*0.75))
        cmds.joint(ankleLeft, e=True, zso=True, oj='xyz')

        cmds.select(clear=True)
        cmds.select(hipCenter)
        hipRight = cmds.joint(p=(-self.sWidthHalf*0.5, self.secHeight + (self.secHeight/10.0)/2.0, 0))
        cmds.joint(hipCenter, e=True, zso=True, oj='xyz')
        kneeRight = cmds.joint(p=(-self.sWidthHalf*0.5, self.secHeight/2.0, 0))
        cmds.joint(hipRight, e=True, zso=True, oj='xyz')
        ankleRight = cmds.joint(p=(-self.sWidthHalf*0.5, 0, 0))
        cmds.joint(kneeRight, e=True, zso=True, oj='xyz')
        footRight = cmds.joint(p=(-self.sWidthHalf*0.5, 0, self.sWidthHalf*0.75))
        cmds.joint(ankleRight, e=True, zso=True, oj='xyz')

        return hipCenter, spine, neckBase, shoulderBladeLeft, shoulderLeft, elbowLeft, wristLeft, handLeft, \
               shoulderBladeRight, shoulderRight, elbowRight, wristRight, handRight, hipLeft, kneeLeft, ankleLeft, \
               footLeft, hipRight, kneeRight, ankleRight, footRight
