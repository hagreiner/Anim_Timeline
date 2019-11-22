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

    def rotation(self):
        pass

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
        for touplePack in self.args:
            tempList = []
            for item in touplePack[1]:
                tempList.append(StashPosition.posesDict[touplePack[0]][item])
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

        self.deltaPercent = cmds.floatSliderGrp("deltaScale", query=True, value=True)
        self.armScale = cmds.floatSlider("armScale", query=True, value=True)
        self.legScale = cmds.floatSlider("legScale", query=True, value=True)
        self.tiltScale = cmds.floatSlider("tiltScale", query=True, value=True)

    def load(self):
        posLeftArmOne = StashPosition(jointList=1 * self.armScale, parent="leftShoulder", poseName="posOne",
                                   direction="z", fromA=0).relativeToBasePos()
        posLeftArmTwo = StashPosition(jointList=0.5 * self.armScale, parent="leftShoulder", poseName="posTwo",
                                   direction="z", fromA=1 * self.armScale).relativeToBasePos()
        posRightArmOne = StashPosition(jointList=1 * self.armScale, parent="rightShoulder", poseName="posRightOne",
                                   direction="z", fromA=0).relativeToBasePos()
        posRightArmTwo = StashPosition(jointList=0.5 * self.armScale, parent="rightShoulder", poseName="posRightTwo",
                                   direction="z", fromA=1 * self.armScale).relativeToBasePos()

        posKneeRightOne = StashPosition(jointList=4.0 * self.legScale, parent="rightKnee", poseName="posKneeOne",
                                     direction="x", fromA=1 * self.legScale).relativeToBasePos()
        posKneeRightTwo = StashPosition(jointList=5.5 * self.legScale, parent="rightKnee", poseName="posKneeTwo",
                                    direction="x", fromA=4.0 * self.legScale).relativeToBasePos()
        posKneeLeftOne = StashPosition(jointList=0 * self.legScale, parent="leftKnee", poseName="posKneeLOne",
                                     direction="x", fromA=0 * self.legScale).relativeToBasePos()
        posKneeLeftTwo = StashPosition(jointList=4.0 * self.legScale, parent="leftKnee", poseName="posKneeLTwo",
                                     direction="x", fromA=1 * self.legScale).relativeToBasePos()
        posKneeLeftThree = StashPosition(jointList=5.5 * self.legScale, parent="leftKnee", poseName="posKneeLThree",
                                    direction="x", fromA=4.0 * self.legScale).relativeToBasePos()

        posRightHipOne = StashPosition(jointList=0.1 * self.legScale, parent="rightHip", poseName="posHipRightOne",
                                   direction="x", fromA=0 * self.legScale).relativeToBasePos()
        posRightHipTwo = StashPosition(jointList=2 * self.legScale, parent="rightHip", poseName="posHipRightTwo",
                                   direction="x", fromA=0 * self.legScale).relativeToBasePos()

        posTiltOne = StashPosition(jointList=0.0 * self.tiltScale, parent="hipCenter", poseName="posTiltOne",
                                    direction="y", fromA=0 * self.tiltScale).relativeToBasePos()
        posTiltTwo = StashPosition(jointList=25 * self.tiltScale, parent="hipCenter", poseName="posTiltTwo",
                                    direction="y", fromA=0 * self.tiltScale).relativeToBasePos()
        posTiltThree = StashPosition(jointList=0.0 * self.tiltScale, parent="hipCenter", poseName="posTiltThree",
                                    direction="z", fromA=0 * self.tiltScale).relativeToBasePos()
        posTiltFour = StashPosition(jointList=0.9 * self.tiltScale, parent="hipCenter", poseName="posTiltFour",
                                    direction="z", fromA=0 * self.tiltScale).relativeToBasePos()
        # list or pose keys for lerping well
        CreateDelta(
            posRightHipOne, posLeftArmOne, posRightArmOne, posTiltOne,
        ).addDelta(deltaName="deltaOne")
        CreateDelta(
            # StashPosition.posesDict["posTwo"],
            posLeftArmTwo, posRightArmTwo, posTiltThree, posKneeRightOne, #posKneeRightTwo, posKneeLeftTwo,
        ).addDelta(deltaName="deltaTwo")
        CreateDelta(
            # StashPosition.posesDict["posTwo"],
            posTiltTwo, posTiltFour, posRightHipTwo #posKneeLeftThree
        ).addDelta(deltaName="deltaThree")

        Clips().PosInit(time=0)
        newTime = Clips().Poses(time=0, loadingList="deltaOne")
        newTime = Clips().Poses(time=newTime + 1, loadingList="deltaTwo")
        newTime = Clips().Poses(time=newTime + 1, loadingList="deltaThree")
        # newTime = Clips().Poses(time=newTime + 1, loadingList="deltaOne")
        # cmds.playbackOptions(minTime='0sec', maxTime=str(newTime) + 'sec')


class Clips:
    def PosInit(self, time):
        for jointName, joint in StashPosition.stash.items():
            cmds.setKeyframe(joint["joint"] + '.tx', v=joint["posX"], time=(calcFrames()[time], calcFrames()[time]))
            cmds.setKeyframe(joint["joint"] + '.ty', v=joint["posY"], time=(calcFrames()[time], calcFrames()[time]))
            cmds.setKeyframe(joint["joint"] + '.tz', v=joint["posZ"], time=(calcFrames()[time], calcFrames()[time]))

    def Poses(self, time, loadingList):
        for poseList in CreateDelta.deltaDict[loadingList]:
            time_alt = time
            for pose in poseList:
                for joint, jointDict in pose.items():
                    cmds.setKeyframe(joint, attribute='translateX',
                                     t=calcFrames()[time_alt], v=jointDict["posX"])
                    cmds.setKeyframe(joint, attribute='translateY',
                                     t=calcFrames()[time_alt], v=jointDict["posY"])
                    cmds.setKeyframe(joint, attribute='translateZ',
                                     t=calcFrames()[time_alt], v=jointDict["posZ"])
                time_alt += 1
            time_alt += 1

        return time


class StashPosition:
    basePosDict = {}
    posesDict = {}
    stash = None

    def __init__(self, jointList, poseName, parent, direction, fromA):
        self.jointList = []
        divNum = 0.25
        if direction == "x":
            for x in range(int(jointList/divNum)):
                deg = (x * 1)
                if (fromA >= jointList and deg >= jointList) or (fromA <= jointList and deg >= fromA):
                    self.jointList.append(RotatePos(parent=parent, degree=(x * divNum)).rotX())
            if len(self.jointList) == 0:
                self.jointList = [RotatePos(parent=parent, degree=(0)).rotX()]
        if direction == "y":
            for x in range(int(jointList/divNum)):
                deg = (x * 1)
                if (fromA >= jointList and deg >= jointList) or (fromA <= jointList and deg >= fromA):
                    self.jointList.append(RotatePos(parent=parent, degree=(x * 1)).rotY())
            if len(self.jointList) == 0:
                self.jointList = [RotatePos(parent=parent, degree=(0)).rotY()]
        if direction == "z":
            for x in range(int(jointList/divNum)):
                deg = (x * 1)
                if (fromA >= jointList and deg >= jointList) or (fromA <= jointList and deg >= fromA):
                    self.jointList.append(RotatePos(parent=parent, degree=(x * divNum)).rotZ())
            if len(self.jointList) == 0:
                self.jointList = [RotatePos(parent=parent, degree=(0)).rotZ()]
        self.poseName = poseName

    def relativeToBasePos(self):
        count = 0
        poseNames = []
        StashPosition.posesDict[self.poseName] = {}
        for y in self.jointList:
            poseNames.append(int(count))
            StashPosition.posesDict[self.poseName][int(count)] = {}
            for x in y:
                StashPosition.posesDict[self.poseName][int(count)][x["joint"]] = {"posX": x["posX"], "posY": x["posY"], "posZ": x["posZ"]}
            count += 1

        CreateBuild.skeletonDict = copy.deepcopy(StashPosition.stash)
        return (self.poseName, poseNames)


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = 150
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
    return returnList
