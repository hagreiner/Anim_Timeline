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
        for joint in self.childList:
            angleSin = math.sin(self.rotationDegree)
            angleCos = math.cos(self.rotationDegree)

            joint["posX"] -= self.parent["posX"]
            joint["posZ"] -= self.parent["posZ"]

            tempX = joint["posX"]
            tempZ = joint["posZ"]

            joint["posZ"] = tempZ * angleCos + tempX * angleSin
            joint["posX"] = -1 * tempZ * angleSin + tempX * angleCos

            x_move = joint["posX"] + self.parent["posX"]
            z_move = joint["posZ"] + self.parent["posZ"]

            joint["posX"] = x_move
            joint["posZ"] = z_move

        return self.childList

    def rotX(self):
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
    def __init__(self, parent, movement):
        self.childList = Controls().findChildren(joint=parent)
        self.parent = CreateBuild.skeletonDict[parent]
        self.moveAmount = movement

    def moveX(self):
        self.parent["posX"] += self.moveAmount
        for joint in self.childList:
            joint["posX"] += self.moveAmount

        return self.childList

    def moveY(self):
        self.parent["posY"] += self.moveAmount
        for joint in self.childList:
            joint["posY"] += self.moveAmount

        return self.childList

    def moveZ(self):
        self.parent["posZ"] += self.moveAmount
        for joint in self.childList:
            joint["posZ"] += self.moveAmount

        return self.childList


class CreateDelta:
    deltaDict = {}

    def __init__(self, *args):
        self.args = args

    def addDelta(self, deltaName):
        deltaList = []
        for smallList in self.args:
            tempList = []
            for item in smallList:
                tempList.append(StashPosition.posesDict[item])
            deltaList.append(tempList)

        CreateDelta.deltaDict[deltaName] = deltaList
        # creates a list of dictionaries of joint positions


class Play:
    frameNum = 10
    distX = 0

    def __init__(self):
        reset()
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
        self.deltaPercent = cmds.floatSliderGrp("deltaScale", query=True, value=True)

        posOneList = StashPosition(jointList=30.0 * self.deltaPercent, parent="leftShoulder", poseName="posOne",
                                   direction="y", fromA=0).relativeToBasePos()
        posTwoList = StashPosition(jointList=-90.0 * self.deltaPercent, parent="leftShoulder", poseName="posTwo",
                                   direction="y", fromA=30).relativeToBasePos()
        posThreeList = StashPosition(jointList=30.0 * self.deltaPercent, parent="rightKnee", poseName="posKneeOne",
                                     direction="x", fromA=0).relativeToBasePos()
        posFourList = StashPosition(jointList=0.0 * self.deltaPercent, parent="rightKnee", poseName="posKneeTwo",
                                    direction="x", fromA=30).relativeToBasePos()
        # list or pose keys for lerping well
        CreateDelta(
            posTwoList, posFourList
        ).addDelta(deltaName="deltaOne")
        CreateDelta(
            # StashPosition.posesDict["posTwo"],
            posOneList, posThreeList
        ).addDelta(deltaName="deltaTwo")

        Clips().PosInit(time=0)
        newTime = Clips().Poses(time=1, loadingList="deltaOne")
        newTime = Clips().Poses(time=newTime + 1, loadingList="deltaTwo")
        newTime = Clips().Poses(time=newTime + 1, loadingList="deltaOne")


class Clips:
    def PosInit(self, time):
        for jointName, joint in StashPosition.stash.items():
            cmds.setKeyframe(joint["joint"] + '.tx', v=joint["posX"], time=(calcFrames()[time], calcFrames()[time]))
            cmds.setKeyframe(joint["joint"] + '.ty', v=joint["posY"], time=(calcFrames()[time], calcFrames()[time]))
            cmds.setKeyframe(joint["joint"] + '.tz', v=joint["posZ"], time=(calcFrames()[time], calcFrames()[time]))

    def Poses(self, time, loadingList):
        for poseList in CreateDelta.deltaDict[loadingList]:
            for pose in poseList:
                time_alt = time
                for joint, jointDict in pose.items():
                    cmds.setKeyframe(joint, attribute='translateX',
                                     t=calcFrames()[time_alt], v=jointDict["posX"])
                    cmds.setKeyframe(joint, attribute='translateY',
                                     t=calcFrames()[time_alt], v=jointDict["posY"])
                    cmds.setKeyframe(joint, attribute='translateZ',
                                     t=calcFrames()[time_alt], v=jointDict["posZ"])
                time_alt += 1

        return time


class StashPosition:
    basePosDict = {}
    posesDict = {}
    stash = None

    def __init__(self, jointList, poseName, parent, direction, fromA):
        self.jointList = []
        if direction == "x":
            for x in range(int(jointList/5) + 1):
                deg = (x * 5)
                if (fromA >= jointList and deg >= jointList) or (fromA <= jointList and deg >= fromA):
                    self.jointList.append(RotatePos(parent=parent, degree=(x * 5)).rotX())
            if len(self.jointList) == 0:
                self.jointList = [RotatePos(parent=parent, degree=(0)).rotX()]
        if direction == "y":
            for x in range(int(jointList/10) + 1):
                self.jointList.append(RotatePos(parent=parent, degree=(x * 10)).rotY())
            if len(self.jointList) == 0:
                self.jointList = [RotatePos(parent=parent, degree=(0)).rotY()]
        if direction == "z":
            for x in range(int(jointList/10) + 1):
                self.jointList.append(RotatePos(parent=parent, degree=(x * 10)).rotZ())
            if len(self.jointList) == 0:
                self.jointList = [RotatePos(parent=parent, degree=(0)).rotZ()]
        self.poseName = poseName

    def relativeToBasePos(self):
        count = 1
        poseNames = []
        for y in self.jointList:
            poseName = self.poseName
            poseName += "_" + num2words(count)
            poseNames.append(poseName)
            StashPosition.posesDict[poseName] = {}
            for x in y:
                StashPosition.posesDict[poseName][x["joint"]] = {"posX": x["posX"], "posY": x["posY"], "posZ": x["posZ"]}
            count += 1

        CreateBuild.skeletonDict = copy.deepcopy(StashPosition.stash)
        return poseNames


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = 8
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
    return returnList


def num2words(num):
    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
                'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    if num < 20:
        return under_20[num]