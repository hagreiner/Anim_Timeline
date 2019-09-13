import maya.cmds as cmds
from constants import MAX_TIME, DIV_NUM, DIV
from objects import Plane


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
        Play.distY = cmds.intSliderGrp("distanceYMax", query=True, value=True)
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


def makeFrames():
    for x in range(DIV_NUM/2 - 3):
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", cp=True,
                         t=[calcFrames()[x], calcFrames()[x + 1]], v=0)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", cp=True,
                         t=[calcFrames()[x + 1], calcFrames()[x + 2]], v=Play.distYMax-x)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x) + "].yValue", cp=True,
                         t=[calcFrames()[x + 2], calcFrames()[x + 3]], v=0)

        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x+3) + "].yValue", cp=True,
                         t=[calcFrames()[x], calcFrames()[x + 1]], v=0)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x+3) + "].yValue", cp=True,
                         t=[calcFrames()[x + 1], calcFrames()[x + 2]], v=-Play.distYMax/2.0)
        cmds.setKeyframe(CreateBuild.cube + ".controlPoints[" + str(x+3) + "].yValue", cp=True,
                             t=[calcFrames()[x + 2], calcFrames()[x + 3]], v=0)


def makeFramesVersion2():
    valDict = {
        0: [0],
        1: [1, 9],
        2: [2, 10, 18],
        3: [3, 11, 19, 27],
        4: [0],
        5: [0],
        6: [0],
        7: [0],
        8: [0],
        9: [0],
        10: [0],
        11: [0],
        12: [0],
    }
    cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(0) + "].py",
                     t=[calcFrames()[0], calcFrames()[0 + 1]], v=0)
    cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(0) + "].py",
                     t=[calcFrames()[0], calcFrames()[0 + 1]], v=Play.distYMax)
    cmds.setKeyframe(CreateBuild.plane + ".pt[" + str(0) + "].py",
                     t=[calcFrames()[0], calcFrames()[0 + 1]], v=0)