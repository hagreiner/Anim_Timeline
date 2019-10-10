import maya.cmds as cmds
from constants import MAX_TIME
from objects import CharacterModel
import math


class CreateBuild:
    """
    "joint":joint, "parent":parent, "rotateX":0, "rotateY":0, "rotateZ":0, "posX":xpos, "posY":ypos, "posZ":zpos
    """
    hipCenter = None
    spine = None
    neckBase = None
    shoulderBladeLeft = None
    shoulderLeft = None
    elbowLeft = None
    wristLeft = None
    handLeft = None
    shoulderBladeRight = None
    shoulderRight = None
    elbowRight = None
    wristRight = None
    handRight = None
    hipLeft = None
    kneeLeft = None
    ankleLeft = None
    footLeft = None
    hipRight = None
    kneeRight = None
    ankleRight = None
    footRight = None
    skeletonDict = {}

    def buildObjects(self):
        CreateBuild.hipCenter, CreateBuild.spine, CreateBuild.neckBase, CreateBuild.shoulderBladeLeft, \
        CreateBuild.shoulderLeft, CreateBuild.elbowLeft, CreateBuild.wristLeft, CreateBuild.handLeft, \
        CreateBuild.shoulderBladeRight, CreateBuild.shoulderRight, CreateBuild.elbowRight, \
        CreateBuild.wristRight, CreateBuild.handRight, CreateBuild.hipLeft, CreateBuild.kneeLeft, \
        CreateBuild.ankleLeft, CreateBuild.footLeft, CreateBuild.hipRight, CreateBuild.kneeRight, \
        CreateBuild.ankleRight, CreateBuild.footRight = CharacterModel().make()

        CreateBuild.skeletonDict = {"hipCenter": CreateBuild.hipCenter, "spine":CreateBuild.spine,
                                    "neck":CreateBuild.neckBase, "leftShoulderBlade":CreateBuild.shoulderBladeLeft,
                                    "rightShoulderBlade":CreateBuild.shoulderBladeRight,
                                    "leftShoulder":CreateBuild.shoulderLeft, "rightShoulder":CreateBuild.shoulderRight,
                                    "leftElbow":CreateBuild.elbowLeft, "rightElbow":CreateBuild.elbowRight,
                                    "leftWrist":CreateBuild.wristLeft, "leftHand":CreateBuild.handLeft,
                                    "rightWrist":CreateBuild.wristRight, "rightHand":CreateBuild.handRight,
                                    "leftHip":CreateBuild.hipLeft, "leftKnee":CreateBuild.kneeLeft,
                                    "leftAnkle":CreateBuild.ankleLeft, "leftFoot":CreateBuild.footLeft,
                                    "rightHip":CreateBuild.hipRight, "rightKnee":CreateBuild.kneeRight,
                                    "rightAnkle":CreateBuild.ankleRight, "rightFoot":CreateBuild.footRight}


class Controls:
    def findChildren(self, joint):
        checkList = [CreateBuild.skeletonDict[joint]["joint"]]
        childList = []

        for x in range(len(CreateBuild.skeletonDict)):
            for k, v in CreateBuild.skeletonDict.items():
                if v["parent"] in checkList and v["joint"] not in checkList:
                    checkList.append(v["joint"])
                    childList.append(v)

        return childList


class RotatePos:
    def __init__(self, parent, degree):
        self.childList = Controls().findChildren(joint=parent)
        self.parent = CreateBuild.skeletonDict[parent]
        self.rotationDegree = degree

    def rotY(self):
        cmds.rotate(0, str(self.rotationDegree) + "deg", 0, self.parent["joint"])
        self.parent["rotateY"] = self.rotationDegree
        for joint in self.childList:
            angleSin = math.sin(self.rotationDegree)
            angleCos = math.cos(self.rotationDegree)

            joint["posX"] -= self.parent["posX"]
            joint["posZ"] -= self.parent["posZ"]

            tempX = joint["posX"]
            tempZ = joint["posZ"]

            joint["posX"] = tempX * angleCos + tempZ * angleSin
            joint["posZ"] = -1 * tempX * angleSin + tempZ * angleCos

            x_move = joint["posX"] + self.parent["posX"]
            z_move = joint["posZ"] + self.parent["posZ"]

            cmds.move(x_move, joint["posY"], z_move, joint["joint"])

            joint["posX"] = x_move
            joint["posZ"] = z_move
        return self.childList

    def rotX(self):
        cmds.rotate(str(self.rotationDegree) + "deg", 0, 0, self.parent["joint"])
        self.parent["rotateX"] = self.rotationDegree
        for joint in self.childList:
            angleSin = math.sin(self.rotationDegree)
            angleCos = math.cos(self.rotationDegree)

            joint["posY"] -= self.parent["posY"]
            joint["posZ"] -= self.parent["posZ"]

            tempY = joint["posY"]
            tempZ = joint["posZ"]

            joint["posY"] = tempY * angleCos + tempZ * angleSin
            joint["posZ"] = -1 * tempY * angleSin + tempZ * angleCos

            y_move = joint["posY"] + self.parent["posY"]
            z_move = joint["posZ"] + self.parent["posZ"]

            cmds.move(joint["posX"], y_move, z_move, joint["joint"])

            joint["posY"] = y_move
            joint["posZ"] = z_move
        return self.childList

    def rotZ(self):
        cmds.rotate(0, 0, str(self.rotationDegree) + "deg",  self.parent["joint"])
        self.parent["rotateZ"] = self.rotationDegree
        for joint in self.childList:
            angleSin = math.sin(self.rotationDegree)
            angleCos = math.cos(self.rotationDegree)

            joint["posX"] -= self.parent["posX"]
            joint["posY"] -= self.parent["posY"]

            tempX = joint["posX"]
            tempY = joint["posY"]

            joint["posX"] = tempX * angleCos + tempY * angleSin
            joint["posY"] = -1 * tempX * angleSin + tempY * angleCos

            x_move = joint["posX"] + self.parent["posX"]
            y_move = joint["posY"] + self.parent["posY"]

            cmds.move(x_move, y_move, joint["posZ"], joint["joint"])

            joint["posX"] = x_move
            joint["posY"] = y_move
        return self.childList


class Play:
    frameNum = 10
    distX = 0

    def __init__(self):
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        cmds.playbackOptions(minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        cmds.select(all=True)
        cmds.cutKey(time=(0,MAX_TIME), cl=True)
        cmds.select(clear=True)

    def forwards(self):
        Play().stop()
        LoadClipOne(direction="forward").load()
        cmds.play(forward=True)

    def backwards(self):
        Play().stop()
        LoadClipOne(direction="backwards").load()
        cmds.play(forward=True)

    def stop(self):
        cmds.play(state=False)


class LoadClipOne:
    def __init__(self, direction):
        if direction == "forward":
            self.direction = 0
        else:
            self.direction = Play.distX

    def load(self):
        Clips().PosOne(time=0)
        Clips().PosTwo(time=2)


class Clips:
    def PosOne(self, time):
        keyedList_1 = RotatePos(parent="leftShoulder", degree=30.0).rotY()
        for items in keyedList_1:
            # cmds.keyframe('surface1.translateX',edit=True,index=(1,1),timeChange='1.5sec',valueChange=10.25)
            cmds.setKeyframe(items["joint"] + '.tx', edit=True, time=(calcFrames()[time], calcFrames()[time+1]))
            cmds.setKeyframe(items["joint"] + '.tz', edit=True, time=(calcFrames()[time], calcFrames()[time+1]))
    def PosTwo(self, time):
        keyedList_1 = RotatePos(parent="leftShoulder", degree=-30.0).rotY()
        for items in keyedList_1:
            # cmds.keyframe('surface1.translateX',edit=True,index=(1,1),timeChange='1.5sec',valueChange=10.25)
            cmds.setKeyframe(items["joint"] + '.tx', edit=True, time=(calcFrames()[time], calcFrames()[time+1]))
            cmds.setKeyframe(items["joint"] + '.tz', edit=True, time=(calcFrames()[time], calcFrames()[time+1]))


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = 5
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
    return returnList


def delFrames(object):
    cmds.cutKey(object, time=(0, MAX_TIME), attribute='translateX', option="keys" )
