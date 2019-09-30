import maya.cmds as cmds
from constants import MAX_TIME
from objects import CharacterModel


class CreateBuild:
    hipCenter = None
    spine = None
    neckBase = None
    shoulderBladeLeft = None
    shoulderLeft = None
    elbowLeft = None
    wristLeft = None
    handLeft = None
    shoulderBladeRight = None
    shoulderRight = None
    elbowRight = None
    wristRight = None
    handRight = None
    hipLeft = None
    kneeLeft = None
    ankleLeft = None
    footLeft = None
    hipRight = None
    kneeRight = None
    ankleRight = None
    footRight = None

    def buildObjects(self):
        CreateBuild.hipCenter, CreateBuild.spine, CreateBuild.neckBase, CreateBuild.shoulderBladeLeft, \
        CreateBuild.shoulderLeft, CreateBuild.elbowLeft, CreateBuild.wristLeft, CreateBuild.handLeft, \
        CreateBuild.shoulderBladeRight, CreateBuild.shoulderRight, CreateBuild.elbowRight, \
        CreateBuild.wristRight, CreateBuild.handRight, CreateBuild.hipLeft, CreateBuild.kneeLeft, \
        CreateBuild.ankleLeft, CreateBuild.footLeft, CreateBuild.hipRight, CreateBuild.kneeRight, \
        CreateBuild.ankleRight, CreateBuild.footRight = CharacterModel().make()


class Play:
    frameNum = 10
    distX = 0

    def __init__(self):
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        Play.distX = cmds.intSliderGrp("distanceX", query=True, value=True)
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
        Clips().PosOne(time=0)
        Clips().PosTwo(time=2)
        Clips().PosThree(time=4)
        Clips().PosFour(time=6)
        Clips().PosFive(time=8)
        Clips().PosSix(time=10)
        Clips().PosFive(time=12)
        Clips().PosFour(time=14)
        Clips().PosThree(time=16)
        Clips().PosTwo(time=18)
        Clips().PosOne(time=20)


class Clips:
    def PosOne(self, time):
        cmds.setKeyframe(CreateBuild.hipCenter, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.spine, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderLeft, at="rotateZ", v=90, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.shoulderLeft, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipLeft, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.kneeLeft, at="rotateZ", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderRight, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.shoulderRight, at="rotateZ", v=90, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.hipRight, at="translateX", v=-2.5, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.ankleRight, at="rotateZ", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))

    def PosTwo(self, time):
        cmds.setKeyframe(CreateBuild.hipCenter, at="rotateY", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.spine, at="rotateY", v=-25, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderLeft, at="rotateY", value=0,
                         t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipLeft, at="rotateY", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeLeft, at="rotateZ", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleLeft, at="rotateZ", value=-0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderRight, at="rotateY", value=0,
                         t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.kneeRight, at="rotateY", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.hipRight, at="rotateY", value=14, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.hipRight, at="translateX", v=2.5, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.ankleRight, at="rotateZ", value=-14, t=(calcFrames()[time], calcFrames()[time + 1]))

    def PosThree(self, time):
        cmds.setKeyframe(CreateBuild.hipCenter, at="rotateY", value=-20, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.spine, at="rotateY", v=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderLeft, at="rotateY", value=-30, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipLeft, at="rotateY", value=47, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeLeft, at="rotateZ", value=-65, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderRight, at="rotateY", value=30, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="rotateY", value=-7, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="translateX", v=-2.5, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeRight, at="rotateY", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleRight, at="rotateZ", value=5, t=(calcFrames()[time], calcFrames()[time + 1]))

    def PosFour(self, time):
        cmds.setKeyframe(CreateBuild.hipCenter, at="rotateY", value=-20, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderLeft, at="rotateY", value=-30, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipLeft, at="rotateY", value=47, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeLeft, at="rotateZ", value=-65, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleLeft, at="rotateZ", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderRight, at="rotateY", value=30, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="rotateY", value=-7, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="translateX", v=-2.5, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeRight, at="rotateY", value=20, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleRight, at="rotateZ", value=5, t=(calcFrames()[time], calcFrames()[time + 1]))

    def PosFive(self, time):
        cmds.setKeyframe(CreateBuild.hipCenter, at="rotateY", value=-40, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderLeft, at="rotateY", value=-60,
                         t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipLeft, at="rotateY", value=90, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeLeft, at="rotateZ", value=-120, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleLeft, at="rotateZ", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.shoulderRight, at="rotateY", value=50,
                         t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="rotateY", value=-7, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.kneeRight, at="rotateY", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleRight, at="rotateZ", value=-14,
                         t=(calcFrames()[time], calcFrames()[time + 1]))

    def PosSix(self, time):
        cmds.setKeyframe(CreateBuild.hipLeft, at="rotateY", value=14, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeLeft, at="rotateZ", value=-0, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.ankleLeft, at="rotateZ", value=-14, t=(calcFrames()[time], calcFrames()[time + 1]))

        cmds.setKeyframe(CreateBuild.hipRight, at="rotateY", value=-90, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.kneeRight, at="rotateY", value=120, t=(calcFrames()[time], calcFrames()[time + 1]))
        cmds.setKeyframe(CreateBuild.ankleRight, at="rotateZ", value=0, t=(calcFrames()[time], calcFrames()[time + 1]))


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    frameCount = 22
    returnList = []
    for x in range(frameCount):
        returnList.append((Play.frameNum/frameCount)*x)
    return returnList


def delFrames(object):
    cmds.cutKey(object, time=(0, MAX_TIME), attribute='translateX', option="keys" )
