import maya.cmds as cmds
from constants import MAX_TIME, MIN_TIME
import math
import copy
import logPoses


class CreateBuild:
    curvesLocationDict = None

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
        self.deltaPercentRig = cmds.floatSliderGrp("deltaScaleRig", query=True, value=True)

        self.PoseOneScale = cmds.intSlider("Pose_One_Length", query=True, value=True)
        self.PoseTwoScale = cmds.intSlider("Pose_Two_Length", query=True, value=True)
        self.PoseThreeScale = cmds.intSlider("Pose_Three_Length", query=True, value=True)
        self.PoseFourScale = cmds.intSlider("Pose_Four_Length", query=True, value=True)

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
