import maya.cmds as cmds
from constants import MAX_TIME, DIV
from objects import Plane, StaticObjects, Curves, Bird
import random


class CreateBuild:
    water = None
    curve = None
    bird = None
    birdJoint = None

    def __init__(self):
        # self.linearCurve = cmds.radioButton("linCurve", query=True, select=True)
        self.swoopCurve = cmds.radioButton("swoopCurve", query=True, select=True)
        self.circleCurve = cmds.radioButton("circleCurve", query=True, select=True)

    def buildObjects(self):
        CreateBuild.water = Plane().make()
        StaticObjects().make()
        if self.circleCurve == True:
            CreateBuild.curve = Curves().circle()
        if self.swoopCurve == True:
            CreateBuild.curve = Curves().swoop()
        CreateBuild.bird, CreateBuild.birdJoint = Bird().make()
        # cmds.rotate(0, -80, 0, CreateBuild.birdJoint, relative=True)


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
            delCurveFrames()
            delBoneFrames()
        except:
            pass


    def forwards(self):
        Play().stop()
        LoadClipOne(direction="forward").load()
        cmds.play(forward=True)

    # def backwards(self):
    #     Play().stop()
    #     LoadClipOne(direction="backwards").load()
    #     cmds.play(forward=True)

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
            MakeFramesWater(inputY=wave).make()

        if Play.waveCount > 1:
            findFrames()

        AnimBones().anim()
        AnimCurve().anim()


def reset():
    cmds.currentTime(0, edit=True)


def delFrames():
    for y in range(440):
        cmds.cutKey(CreateBuild.water + ".pt[" + str(y) + "].py", time=(0, MAX_TIME), option="keys")


def delCurveFrames():
    cmds.select(CreateBuild.bird)
    cmds.delete(mp=True)


def delBoneFrames():
    cmds.cutKey(CreateBuild.birdJoint, time=(0, MAX_TIME), option="keys")


class MakeFramesWater:
    def __init__(self, inputY):
        self.input = inputY
        self.y = inputY
        self.boolList = [-1, 0, 1]
        self.offsetList = list(range(0, 5))

    def make(self):
        for x in range(441):
            self.y += random.choice(self.offsetList)
            value = (random.choice(determineRange()) * random.choice(self.boolList))
            # cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
            #                  t=[calcFrames()[self.y], calcFrames()[self.y + 1]], v=0)
            cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
                             t=[calcFrames()[self.y], calcFrames()[self.y + 10]],
                             v=value)
            # cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
            #                      t=[calcFrames()[self.y + 12], calcFrames()[self.y + 12]], v=0)
            self.y = self.input


class AnimCurve:
    def anim(self):
        cmds.pathAnimation(CreateBuild.bird, c=CreateBuild.curve, stu=0, etu=Play.frameNum, f=True, ua="z", fm=True,
                           bankScale=-4, fa='y')
        # cmds.pathAnimation(CreateBuild.bird, c=CreateBuild.curve, stu=0, etu=Play.frameNum, f=True, ua="x", fm=True,
        #                    bankScale=-90)


class AnimBones:
    def anim(self):
        value = 0
        for x in range(len(calcFrames()) - 1):
            if x%2 == 0:
                value = 0
            if x%2 == 1:
                value = 1
            cmds.setKeyframe(CreateBuild.birdJoint + ".rotate", cp=True, breakdown=True, at="rotationY",
                             time=(calcFrames()[x], calcFrames()[x+1]), v=70*value)


def findFrames():
    for x in range(441):
        frame = cmds.findKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", time=(0, MAX_TIME), which="first")
        cmds.selectKey(CreateBuild.water + ".pt[" + str(x) + "].py", time=(frame, frame))
        value = cmds.keyframe(query=True, sl=True, valueChange=True)
        value = float(value[0])
        cmds.setKeyframe(CreateBuild.water + ".pt[" + str(x) + "].py", cp=True, breakdown=True,
                         time=(calcFrames()[-1], calcFrames()[-1]), v=value)


def calcFrames():
    frames = 25
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
