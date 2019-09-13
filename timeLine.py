import maya.cmds as cmds
from constants import MAX_TIME, DIV
from objects import Plane
import random


class CreateBuild:
    water = None

    def buildObjects(self):
        CreateBuild.water = Plane().make()


class Play:
    frameNum = 10
    distYMax = 0
    distYMin = 0
    waveCount = 0

    def __init__(self):
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        Play.distYMax = cmds.intSliderGrp("distanceYMax", query=True, value=True)
        Play.distY = cmds.intSliderGrp("distanceYMin", query=True, value=True)
        Play.waveCount = cmds.intSliderGrp("numWaves", query=True, value=True)
        cmds.playbackOptions(minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        try:
            delFrames()
        except:
            pass

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
            self.direction = Play.distYMax

    def load(self):
        for wave in range(Play.waveCount):
            makeFramesWater()


def reset():
    cmds.currentTime(0, edit=True)


def delFrames():
    for y in range((DIV + 1)*9):
        cmds.cutKey(CreateBuild.water + ".pt[" + str(y) + "].py", time=(0, MAX_TIME), option="keys")


def makeFramesWater():
    for y in range(20):
        for x in range(440):
            cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
                             t=[calcFrames()[y], calcFrames()[y + 10]], v=0)
            cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
                             t=[calcFrames()[y + 10], calcFrames()[y + 20]], v=-(random.choice(determineRange()))/4.0)

            cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
                             t=[calcFrames()[y + 20], calcFrames()[y + 30]], v=random.choice(determineRange()))
            cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
                             t=[calcFrames()[y + 30], calcFrames()[y + 40]], v=0)


def calcFrames():
    frames = 60
    returnList = []
    for x in range(frames):
        returnList.append(((Play.frameNum/frames)*x))
    return returnList


def determineRange():
    if Play.distYMax > Play.distYMin:
        return list(range(Play.distYMin, Play.distYMax))
    elif Play.distYMax < Play.distYMin:
        return list(range(Play.distYMax, Play.distYMin))
    else:
        return [Play.distYMax, Play.distYMax]


# CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue"
