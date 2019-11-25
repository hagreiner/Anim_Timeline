import maya.cmds as cmds
from constants import MAX_TIME
from objects import CharacterModel
import math
import copy


class CreateBuild:
    def buildObjects(self):
        CharacterModel().makeRig()


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
        Clips().PosInit(time=0)
        newTime = Clips().Poses(time=0, loadingList="deltaOne")
        newTime = Clips().Poses(time=newTime + 1, value="deltaTwo", joint=NOPE)
        # cmds.playbackOptions(minTime='0sec', maxTime=str(newTime) + 'sec')


class Clips:
    def PosInit(self, time):
        pass

    def Poses(self, time, joint, value):
        cmds.setKeyframe(joint, attribute='translateX',
                                     t=calcFrames()[time], v=value["posX"])
        cmds.setKeyframe(joint, attribute='translateY',
                                     t=calcFrames()[time], v=value["posY"])
        cmds.setKeyframe(joint, attribute='translateZ',
                                     t=calcFrames()[time], v=value["posZ"])


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = 150
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
    return returnList
