import maya.cmds as cmds
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


class Play:
    frameNum = 10

    def __init__(self):
        reset()
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        cmds.playbackOptions(minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        cmds.select(all=True)
        cmds.cutKey(time=(0, MAX_TIME), cl=True)
        cmds.select(clear=True)

    def forwards(self):
        Play().stop()
        LoadClipOne(direction="forward").load()
        cmds.play(forward=True)

    def stop(self):
        cmds.play(state=False)


class LoadClipOne:
    def __init__(self, direction):
        self.deltaPercent = cmds.floatSliderGrp("deltaScale", query=True, value=True)

    def load(self):

        Clips().Poses(time=0, value=valuesList(0, 0, -20, 1), joint=CreateBuild.lowerHandle)
        Clips().Poses(time=0, value=valuesList(0, 0, -40, 1), joint=CreateBuild.upperHandle)

        newTime = Clips().Poses(time=1, value=valuesList(20, 0, 0, self.deltaPercent), joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(0, 0, -20, self.deltaPercent), joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(-20, 0, 0, self.deltaPercent), joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(0, 0, -20, self.deltaPercent), joint=CreateBuild.lowerHandle)
        newTime = Clips().Poses(time=1, value=valuesList(0, 0, -40, self.deltaPercent), joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(40, 0, -40, self.deltaPercent), joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(0, 0, -40, self.deltaPercent), joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(-40, 0, -40, self.deltaPercent), joint=CreateBuild.upperHandle)
        newTime = Clips().Poses(time=newTime, value=valuesList(0, 0, -40, self.deltaPercent), joint=CreateBuild.upperHandle)


class Clips:
    def Poses(self, time, joint, value):
        print(value)
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


# class RotatePos:
#     def __init__(self, degree, parentLocation, joint):
#         self.rotationDegree = degree
#         self.joint = joint
#
#     def rotation(self):
#
#
#         return None
