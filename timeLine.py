import maya.cmds as cmds
from constants import MAX_TIME, MIN_TIME
from objects import CharacterModel
import math
import copy
import logPoses


class CreateBuild:
    rootJoint = None
    lowerHandle = None
    upperHandle = None
    curvesLocationDict = None

    def buildWavy(self):
        CreateBuild.rootJoint, CreateBuild.lowerHandle, CreateBuild.upperHandle = CharacterModel().makeRig()

    def moveCurves(self):
        CreateBuild.curvesLocationDict = logPoses.findPoseInformation.PosesDict
        print(CreateBuild.curvesLocationDict)


class Play:
    frameNum = 10

    def __init__(self):
        reset()
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        cmds.playbackOptions(minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        cmds.select(all=True)
        cmds.cutKey(time=(0, MAX_TIME), cl=True)
        cmds.select(clear=True)
        self.deltaPercent = cmds.floatSliderGrp("deltaScale", query=True, value=True)
        self.deltaPercentRig = cmds.floatSliderGrp("deltaScaleRig", query=True, value=True)

        self.PoseOneScale = cmds.intSlider("Pose_One_Length", query=True, value=True)
        self.PoseTwoScale = cmds.intSlider("Pose_Two_Length", query=True, value=True)
        self.PoseThreeScale = cmds.intSlider("Pose_Three_Length", query=True, value=True)
        self.PoseFourScale = cmds.intSlider("Pose_Four_Length", query=True, value=True)

    def forwardsWavy(self):
        cmds.move(0, 0, -20, CreateBuild.lowerHandle)
        cmds.move(0, 0, -40, CreateBuild.upperHandle)
        xAxis = cmds.radioButton('xAxis', query=True, select=True)
        yAxis = cmds.radioButton('yAxis', query=True, select=True)
        self.xAxis = 0
        self.yAxis = 0
        self.zAxis = 0

        if xAxis == True:
            self.xAxis = 1
        elif yAxis == True:
            self.yAxis = 1

        Play().stop()
        LoadClips().loadWavy()
        LoadClips().runWavy()
        cmds.play(forward=True)

    def forwardsRig(self):
        Frames.frameCount = 5 + self.PoseOneScale + self.PoseTwoScale + self.PoseThreeScale + self.PoseFourScale
        cmds.playbackOptions(minTime='0sec', maxTime=str(Frames.frameCount/30.0) + 'sec')
        Play().stop()
        LoadClips().loadRig()
        LoadClips().runRig()
        cmds.play(forward=True)

    def stop(self):
        cmds.play(state=False)


class LoadClips(Play):
    def loadWavy(self):
        LoadClips.base_Low = RotatePos(
            0*self.deltaPercent*self.xAxis, 0*self.deltaPercent*self.yAxis, 0*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.base_Up = RotatePos(
            0*self.deltaPercent*self.xAxis, 0*self.deltaPercent*self.yAxis, 0*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()

        LoadClips.baseOff_Low = RotatePos(
            5*self.deltaPercent*self.xAxis, 5*self.deltaPercent*self.yAxis, 5*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.baseOff_Up = RotatePos(
            -5*self.deltaPercent*self.xAxis, -5*self.deltaPercent*self.yAxis, -5*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()

        LoadClips.longRotation_Low_Pos = RotatePos(
            80*self.deltaPercent*self.xAxis, 80*self.deltaPercent*self.yAxis, 80*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.midRotation_Low_Pos = RotatePos(
            35*self.deltaPercent*self.xAxis, 35*self.deltaPercent*self.yAxis, 35*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.longRotation_Low_Neg = RotatePos(
            -80*self.deltaPercent*self.xAxis, -80*self.deltaPercent*self.yAxis, -80*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.midRotation_Low_Neg = RotatePos(
            -35*self.deltaPercent*self.xAxis, -35*self.deltaPercent*self.yAxis, -35*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()

        LoadClips.longRotation_Up_Pos = RotatePos(
            100*self.deltaPercent*self.xAxis, 100*self.deltaPercent*self.yAxis, 100*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()
        LoadClips.midRotation_Up_Pos = RotatePos(
            60*self.deltaPercent * self.xAxis, 60*self.deltaPercent * self.yAxis, 60*self.deltaPercent * self.zAxis,
            CreateBuild.upperHandle).xformRot()
        LoadClips.longRotation_Up_Neg = RotatePos(
            -100*self.deltaPercent*self.xAxis, -100*self.deltaPercent*self.yAxis, -100*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()
        LoadClips.midRotation_Up_Neg = RotatePos(
            -60*self.deltaPercent * self.xAxis, -60*self.deltaPercent * self.yAxis, -60*self.deltaPercent * self.zAxis,
            CreateBuild.upperHandle).xformRot()

    def runWavy(self):
        newTime = Clips().Poses(startTime=0, endtime=1, value=LoadClips.base_Low, joint=CreateBuild.lowerHandle)

        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Low_Pos, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.longRotation_Low_Pos, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Low_Pos, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.baseOff_Low, joint=CreateBuild.lowerHandle)

        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Low_Neg, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.longRotation_Low_Neg, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Low_Neg, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.base_Low, joint=CreateBuild.lowerHandle)


        newTime = Clips().Poses(startTime=0, endtime=1, value=LoadClips.base_Up, joint=CreateBuild.upperHandle)

        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Up_Pos, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.longRotation_Up_Pos, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Up_Pos, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.baseOff_Up, joint=CreateBuild.upperHandle)

        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Up_Neg, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.longRotation_Up_Neg, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.midRotation_Up_Neg, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(startTime=newTime, endtime=newTime+1, value=LoadClips.base_Up, joint=CreateBuild.upperHandle)

    def loadRig(self):
        LoadClips.PoseOne = CreateBuild.curvesLocationDict["Pose_One"]
        LoadClips.PoseTwo = CreateBuild.curvesLocationDict["Pose_Two"]
        LoadClips.PoseThree = CreateBuild.curvesLocationDict["Pose_Three"]
        LoadClips.PoseFour = CreateBuild.curvesLocationDict["Pose_Four"]

    def runRig(self):
        newTime = 1
        for nurbs, location in LoadClips.PoseOne.items():
            Clips().Poses(startTime=newTime, endtime=newTime+self.PoseOneScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseOneScale)
        for nurbs, location in LoadClips.PoseTwo.items():
            Clips().Poses(startTime=newTime, endtime=newTime+self.PoseTwoScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseTwoScale)
        for nurbs, location in LoadClips.PoseThree.items():
            Clips().Poses(startTime=newTime, endtime=newTime+self.PoseThreeScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseThreeScale)
        for nurbs, location in LoadClips.PoseFour.items():
            Clips().Poses(startTime=newTime, endtime=newTime+self.PoseFourScale, value=location, joint=nurbs)


class Clips:
    def Poses(self, startTime, endtime, joint, value):
        cmds.setKeyframe(joint, attribute='translateX', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[0])
        cmds.setKeyframe(joint, attribute='translateY', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[1])
        cmds.setKeyframe(joint, attribute='translateZ', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[2])
        return startTime + 2


def reset():
    cmds.currentTime(0, edit=True)


class Frames:
    frameCount = MIN_TIME
    def calcFrames(self):
        returnList = []
        for x in range(Frames.frameCount):
            returnList.append((Play.frameNum/Frames.frameCount)*x)
        return returnList


def valuesList(X, Y, Z, percent):
    return [(X*percent), (Y*percent), (Z*percent)]


class RotatePos:
    def __init__(self, x, y, z, handle):
        self.parent = {"posX": 0, "posY": 0, "posZ": 0,}
        self.handle = handle
        self.rotX = x
        self.rotY = y
        self.rotZ = z

    def xformRot(self):
        cmds.rotate(self.rotX, self.rotY, self.rotZ, self.handle,
                    pivot=(self.parent["posX"], self.parent["posY"], self.parent["posZ"]))
        location = cmds.xform(self.handle, query=True, bb=True)
        cmds.rotate(0, 0, 0, self.handle, pivot=(self.parent["posX"], self.parent["posY"], self.parent["posZ"]))

        return [(location[0] + location[3])/2.0, (location[1] + location[4])/2.0, (location[2] + location[5])/2.0]
