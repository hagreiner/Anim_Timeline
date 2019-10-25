import maya.cmds as cmds
from constants import MAX_TIME
from objects import CharacterModel
import math
import copy


class CreateBuild:
    """
    "joint":joint, "parent":parent, "rotateX":0, "rotateY":0, "rotateZ":0, "posX":xpos, "posY":ypos, "posZ":zpos
    """
    skeletonDict = {}

    def buildObjects(self):
        hipCenter, spine, neckBase, shoulderBladeLeft, shoulderLeft, elbowLeft, wristLeft, handLeft, \
        shoulderBladeRight, shoulderRight, elbowRight, wristRight, handRight, hipLeft, kneeLeft, \
        ankleLeft, footLeft, hipRight, kneeRight, ankleRight, footRight = CharacterModel().make()

        initialDict = {"hipCenter": hipCenter, "spine": spine, "neck": neckBase, "leftShoulderBlade": shoulderBladeLeft,
                       "rightShoulderBlade": shoulderBladeRight, "leftShoulder": shoulderLeft,
                       "rightShoulder": shoulderRight, "leftElbow": elbowLeft, "rightElbow": elbowRight,
                       "leftWrist": wristLeft, "leftHand": handLeft, "rightWrist": wristRight, "rightHand": handRight,
                       "leftHip": hipLeft, "leftKnee": kneeLeft, "leftAnkle": ankleLeft, "leftFoot": footLeft,
                       "rightHip": hipRight, "rightKnee": kneeRight, "rightAnkle": ankleRight, "rightFoot": footRight}

        CreateBuild.skeletonDict = initialDict
        StashPosition.stash = copy.deepcopy(CreateBuild.skeletonDict)

        for jointName, joint in CreateBuild.skeletonDict.items():
            StashPosition.basePosDict[joint["joint"]] = {"posX": joint["posX"], "posY": joint["posY"], "posZ": joint["posZ"]}
        StashPosition.posesDict["base"] = StashPosition.basePosDict

        StashPosition(jointList=RotatePos(parent="leftShoulder", degree=-30.0).rotY(), poseName="posOne").relativeToBasePos()
        StashPosition(jointList=RotatePos(parent="leftShoulder", degree=0).rotY(), poseName="posTwo").relativeToBasePos()
        StashPosition(jointList=RotatePos(parent="leftShoulder", degree=-30.0).rotY(), poseName="posThree").relativeToBasePos()
        StashPosition(jointList=RotatePos(parent="rightKnee", degree=30.0).rotX(), poseName="posKneeOne").relativeToBasePos()
        StashPosition(jointList=RotatePos(parent="rightKnee", degree=0).rotX(), poseName="posKneeTwo").relativeToBasePos()


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

            joint["posX"] = x_move
            joint["posZ"] = z_move

        return self.childList

    def rotX(self):
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

            joint["posY"] = y_move
            joint["posZ"] = z_move

        return self.childList

    def rotZ(self):
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

            joint["posX"] = x_move
            joint["posY"] = y_move

        return self.childList


class MovePos:
    def __init__(self):
        pass

    def moveX(self):
        pass

    def moveY(self):
        pass

    def moveZ(self):
        pass


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
        Clips().PosInit(time=0)
        Clips().Poses(time=1, loadingList=["base", "posOne", "posTwo", "posThree"])
        Clips().Poses(time=1, loadingList=["base", "posKneeOne", "posKneeTwo", "posKneeOne"])


class Clips:
    def PosInit(self, time):
        for jointName, joint in CreateBuild.skeletonDict.items():
            cmds.setKeyframe(joint["joint"] + '.tx', edit=True, time=(calcFrames()[time], calcFrames()[time]))
            cmds.setKeyframe(joint["joint"] + '.ty', edit=True, time=(calcFrames()[time], calcFrames()[time]))
            cmds.setKeyframe(joint["joint"] + '.tz', edit=True, time=(calcFrames()[time], calcFrames()[time]))

    def Poses(self, time, loadingList):
        num = 0
        for pose in loadingList:
            num += 1
            for joint in StashPosition.posesDict[pose]:
                cmds.setKeyframe(joint, attribute='translateX',
                                 t=[calcFrames()[time + num], calcFrames()[time + num + 1]],
                                 v=StashPosition.posesDict[pose][joint]["posX"])
                cmds.setKeyframe(joint, attribute='translateY',
                                 t=[calcFrames()[time + num], calcFrames()[time + num + 1]],
                                 v=StashPosition.posesDict[pose][joint]["posY"])
                cmds.setKeyframe(joint, attribute='translateZ',
                                 t=[calcFrames()[time + num], calcFrames()[time + num + 1]],
                                 v=StashPosition.posesDict[pose][joint]["posZ"])


class StashPosition:
    basePosDict = {}
    posesDict = {}
    stash = None

    def __init__(self, jointList, poseName):
        self.jointList = jointList
        self.poseName = poseName
        StashPosition.posesDict[self.poseName] = {}

    def relativeToBasePos(self):
        for x in self.jointList:
            StashPosition.posesDict[self.poseName][x["joint"]] = {"posX": x["posX"], "posY": x["posY"], "posZ": x["posZ"]}

        CreateBuild.skeletonDict = StashPosition.stash


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = 8
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
    return returnList
