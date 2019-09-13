import maya.cmds as cmds
from constants import MAX_TIME, DIV_NUM, DIV
from objects import Plane
import random


class CreateBuild:
    cube = None
    plane = None

    def buildObjects(self):
        CreateBuild.cube, CreateBuild.plane = Plane().make()


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
            makeFrames()
            makeFramesVersion2()


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frames = DIV_NUM/2 + 2
    returnList = []
    for x in range(frames):
        returnList.append(((Play.frameNum/frames)*x))
    return returnList


def delFrames():
    for x in range(DIV_NUM/2 - 1):
        cmds.cutKey(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", time=(0, MAX_TIME), option="keys")
    for y in range(81):
        cmds.cutKey(CreateBuild.plane + ".pt[" + str(y) + "].py", time=(0, MAX_TIME), option="keys")


def makeFrames():
    for x in range(DIV_NUM/2 - 3):
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", cp=True,
                         t=[calcFrames()[x], calcFrames()[x + 1]], v=0)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", cp=True,
                         t=[calcFrames()[x + 1], calcFrames()[x + 2]], v=(random.choice(determineRange()))-x)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", cp=True,
                         t=[calcFrames()[x + 2], calcFrames()[x + 3]], v=0)

        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x+3) + "].yValue", cp=True,
                         t=[calcFrames()[x], calcFrames()[x + 1]], v=0)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x+3) + "].yValue", cp=True,
                         t=[calcFrames()[x + 1], calcFrames()[x + 2]], v=-(random.choice(determineRange()))/2.0)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x+3) + "].yValue", cp=True,
                             t=[calcFrames()[x + 2], calcFrames()[x + 3]], v=0)


def makeFramesVersion2():
    valDict = {
        0: [0],
        1: [1, DIV + 1],
        2: [2, DIV + 2, (DIV + 1)*2],
        3: [3, DIV + 3, ((DIV + 1)*2) + 1, (DIV + 1)*3],
        4: [4, DIV + 4, ((DIV + 1)*2) + 2, ((DIV + 1)*3) + 1, (DIV + 1)*4],
        5: [5, DIV + 5, ((DIV + 1)*2) + 3, ((DIV + 1)*3) + 2, ((DIV + 1)*4) + 1, (DIV + 1)*5],
        6: [6, DIV + 6, ((DIV + 1)*2) + 4, ((DIV + 1)*3) + 3, ((DIV + 1)*4) + 2, ((DIV + 1)*5) + 1, (DIV + 1)*6],
        7: [7, DIV + 7, ((DIV + 1)*2) + 5, ((DIV + 1)*3) + 4, ((DIV + 1)*4) + 3, ((DIV + 1)*5) + 2, ((DIV + 1)*6) + 1, (DIV + 1)*7],
        8: [8, DIV + 8, ((DIV + 1)*2) + 6, ((DIV + 1)*3) + 5, ((DIV + 1)*4) + 4, ((DIV + 1)*5) + 3, ((DIV + 1)*6) + 2, ((DIV + 1)*7) + 1, (DIV + 1)*8],
        9: [DIV + 9, ((DIV + 1)*2) + 7, ((DIV + 1)*3) + 6, ((DIV + 1)*4) + 5, ((DIV + 1)*5) + 4, ((DIV + 1)*6) + 3, ((DIV + 1)*7) + 2, ((DIV + 1)*8) + 1],
        10: [((DIV + 1)*2) + 8, ((DIV + 1)*3) + 7, ((DIV + 1)*4) + 6, ((DIV + 1)*5) + 5, ((DIV + 1)*6) + 4, ((DIV + 1)*7) + 3, ((DIV + 1)*8) + 2],
        11: [((DIV + 1)*3) + 8, ((DIV + 1)*4) + 7, ((DIV + 1)*5) + 6, ((DIV + 1)*6) + 5, ((DIV + 1)*7) + 4, ((DIV + 1)*8) + 3],
        12: [((DIV + 1)*4) + 8, ((DIV + 1)*5) + 7, ((DIV + 1)*6) + 6, ((DIV + 1)*7) + 5, ((DIV + 1)*8) + 4],
        13: [((DIV + 1)*5) + 8, ((DIV + 1)*6) + 7, ((DIV + 1)*7) + 6, ((DIV + 1)*8) + 5],
        14: [((DIV + 1)*6) + 8, ((DIV + 1)*7) + 7, ((DIV + 1)*8) + 6],
        15: [((DIV + 1)*7) + 8, ((DIV + 1)*8) + 7],
        16: [((DIV + 1)*8) + 8],
    }
    for x in valDict:
        for vtx in valDict[x]:
            cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(vtx) + "].py", cp=True, breakdown=True,
                             t=[calcFramesV2()[x], calcFramesV2()[x + 1]], v=0)
            cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(vtx) + "].py", cp=True, breakdown=True,
                             t=[calcFramesV2()[x + 1], calcFramesV2()[x + 2]], v=-(random.choice(determineRange()))/4.0)

            cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(vtx) + "].py", cp=True, breakdown=True,
                             t=[calcFramesV2()[x + 2], calcFramesV2()[x + 3]], v=random.choice(determineRange()))
            cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(vtx) + "].py", cp=True, breakdown=True,
                             t=[calcFramesV2()[x + 3], calcFramesV2()[x + 4]], v=0)


def calcFramesV2():
    frames = 16 + 5
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