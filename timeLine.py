import maya.cmds as cmds
import maya.api.OpenMaya as om
from constants import MAX_TIME, MIN_TIME
from objects import CharacterModel
import math
import copy


class CreateBuild:
    rootJoint = None
    lowerHandle = None
    upperHandle = None

    def buildObjects(self):
        CreateBuild.rootJoint, CreateBuild.lowerHandle, CreateBuild.upperHandle = CharacterModel().makeRig()
        # characterMesh = CharacterModel().mesh()
        # cmds.skinCluster(CreateBuild.rootJoint, characterMesh, skinMethod=1)


class Play:
    frameNum = 10

    def __init__(self):
        reset()
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        cmds.playbackOptions(minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        cmds.select(all=True)
        cmds.cutKey(time=(0, MAX_TIME), cl=True)
        cmds.select(clear=True)
        cmds.move(0, 0, -20, CreateBuild.lowerHandle)
        cmds.move(0, 0, -40, CreateBuild.upperHandle)

        self.deltaPercent = cmds.floatSliderGrp("deltaScale", query=True, value=True)

        xAxis = cmds.radioButton('xAxis', query=True, select=True)
        yAxis = cmds.radioButton('yAxis', query=True, select=True)
        self.xAxis = 0
        self.yAxis = 0
        self.zAxis = 0

        if xAxis == True:
            self.xAxis = 1
        elif yAxis == True:
            self.yAxis = 1

    def forwards(self):
        Play().stop()
        LoadClips().load()
        LoadClips().run()
        cmds.play(forward=True)

    def stop(self):
        cmds.play(state=False)


class LoadClips(Play):
    def load(self):
        LoadClips.base_Low = RotatePos(
            0*self.deltaPercent*self.xAxis, 0*self.deltaPercent*self.yAxis, 0*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.base_Up = RotatePos(
            0*self.deltaPercent*self.xAxis, 0*self.deltaPercent*self.yAxis, 0*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()

        LoadClips.longRotation_Low_Pos = RotatePos(
            90*self.deltaPercent*self.xAxis, 90*self.deltaPercent*self.yAxis, 90*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.midRotation_Low_Pos = RotatePos(
            35*self.deltaPercent*self.xAxis, 35*self.deltaPercent*self.yAxis, 35*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.longRotation_Low_Neg = RotatePos(
            -90*self.deltaPercent*self.xAxis, -90*self.deltaPercent*self.yAxis, -90*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()
        LoadClips.midRotation_Low_Neg = RotatePos(
            -35*self.deltaPercent*self.xAxis, -35*self.deltaPercent*self.yAxis, -35*self.deltaPercent*self.zAxis,
            CreateBuild.lowerHandle).xformRot()

        LoadClips.longRotation_Up_Pos = RotatePos(
            90*self.deltaPercent*self.xAxis, 90*self.deltaPercent*self.yAxis, 90*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()
        LoadClips.midRotation_Up_Pos = RotatePos(
            60*self.deltaPercent * self.xAxis, 60*self.deltaPercent * self.yAxis, 60*self.deltaPercent * self.zAxis,
            CreateBuild.upperHandle).xformRot()
        LoadClips.longRotation_Up_Neg = RotatePos(
            -90*self.deltaPercent*self.xAxis, -90*self.deltaPercent*self.yAxis, -90*self.deltaPercent*self.zAxis,
            CreateBuild.upperHandle).xformRot()
        LoadClips.midRotation_Up_Neg = RotatePos(
            -60*self.deltaPercent * self.xAxis, -60*self.deltaPercent * self.yAxis, -60*self.deltaPercent * self.zAxis,
            CreateBuild.upperHandle).xformRot()

    def run(self):
        Clips().Poses(time=0, value=LoadClips.base_Low, joint=CreateBuild.lowerHandle)
        Clips().Poses(time=0, value=LoadClips.base_Up, joint=CreateBuild.upperHandle)

        newTime = Clips().Poses(time=1, value=LoadClips.midRotation_Low_Pos, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.longRotation_Low_Pos, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.midRotation_Low_Pos, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.base_Low, joint=CreateBuild.lowerHandle)

        newTime = Clips().Poses(time=newTime, value=LoadClips.midRotation_Low_Neg, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.longRotation_Low_Neg, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.midRotation_Low_Neg, joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.base_Low, joint=CreateBuild.lowerHandle)

        newTime = Clips().Poses(time=1, value=LoadClips.midRotation_Up_Pos, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.longRotation_Up_Pos, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.midRotation_Up_Pos, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.base_Up, joint=CreateBuild.upperHandle)

        newTime = Clips().Poses(time=newTime, value=LoadClips.midRotation_Up_Neg, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.longRotation_Up_Neg, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.midRotation_Up_Neg, joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=LoadClips.base_Up, joint=CreateBuild.upperHandle)


class Clips:
    def Poses(self, time, joint, value):
        cmds.setKeyframe(joint, attribute='translateX', t=(calcFrames()[time], calcFrames()[time+1]), v=value[0])
        cmds.setKeyframe(joint, attribute='translateY', t=(calcFrames()[time], calcFrames()[time+1]), v=value[1])
        cmds.setKeyframe(joint, attribute='translateZ', t=(calcFrames()[time], calcFrames()[time+1]), v=value[2])
        return time + 2


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = MIN_TIME
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
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