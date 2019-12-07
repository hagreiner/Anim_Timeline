import maya.cmds as cmds
from constants import MAX_TIME, MIN_TIME
import logPoses
import poseLibrary


class CreateBuild:
    curvesLocationDict = None

    def moveCurves(self):
        CreateBuild.curvesLocationDict = logPoses.findPoseInformation.PosesDict


class Play:
    frameNum = 10
    preSet = None

    def __init__(self):
        reset()
        Play.frameNum = cmds.intSlider("frameNum", query=True, value=True)
        cmds.playbackOptions(minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        cmds.select(all=True)
        cmds.cutKey(time=(0, MAX_TIME), cl=True)
        cmds.select(clear=True)
        self.deltaScaleArms = cmds.floatSliderGrp("deltaScaleArms", query=True, value=True)
        self.deltaScaleLegs = cmds.floatSliderGrp("deltaScaleLegs", query=True, value=True)
        self.deltaScaleCore = cmds.floatSliderGrp("deltaScaleCore", query=True, value=True)

        self.PoseOneScale = cmds.intSlider("Pose_One_Length", query=True, value=True)
        self.PoseTwoScale = cmds.intSlider("Pose_Two_Length", query=True, value=True)
        self.PoseThreeScale = cmds.intSlider("Pose_Three_Length", query=True, value=True)
        self.PoseFourScale = cmds.intSlider("Pose_Four_Length", query=True, value=True)

        self.walking = cmds.radioButton('walkingAnim', query=True, select=True)

    def forwardsRig(self):
        Frames.frameCount = 5 + self.PoseOneScale + self.PoseTwoScale + self.PoseThreeScale + self.PoseFourScale
        Play().stop()
        cmds.playbackOptions(minTime='0sec', maxTime=str(Frames.frameCount/30.0) + 'sec')
        LoadClips().loadRig()
        LoadClips().runRig()
        cmds.play(forward=True)

    def forwardsPreSetClip(self):
        clip_move, clip_rot = LoadClips().loadPreSet()
        Frames.frameCount = len(clip_move["arms"].keys()) + 1
        Play().stop()
        cmds.playbackOptions(minTime='0sec', maxTime=str(Frames.frameCount / 30.0) + 'sec')
        LoadClips().runPreSet(clipsDictMove=clip_move, clipsDictRot=clip_rot)
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
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseOneScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseOneScale)
        for nurbs, location in LoadClips.PoseTwo.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseTwoScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseTwoScale)
        for nurbs, location in LoadClips.PoseThree.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseThreeScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseThreeScale)
        for nurbs, location in LoadClips.PoseFour.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseFourScale, value=location, joint=nurbs)

    def loadPreSet(self):
        if self.walking == True:
            return poseLibrary.walking()

    def runPreSet(self, clipsDictMove, clipsDictRot):
        newTime = 0
        for key, nurbsList in clipsDictMove["arms"].items():
            newTime += 1
            for nurbs, location in nurbsList.items():
                Clips().PosesTranslate(startTime=newTime, endtime=newTime,
                                       value=valuesList(location[0], location[1], location[2], self.deltaScaleArms), joint=nurbs)
        newTime = 0
        for key, nurbsList in clipsDictMove["legs"].items():
            newTime += 1
            for nurbs, location in nurbsList.items():
                Clips().PosesTranslate(startTime=newTime, endtime=newTime,
                                       value=valuesList(location[0], location[1], location[2], self.deltaScaleLegs), joint=nurbs)
        newTime = 0
        for key, nurbsList in clipsDictMove["core"].items():
            newTime += 1
            for nurbs, location in nurbsList.items():
                Clips().PosesTranslate(startTime=newTime, endtime=newTime,
                                       value=valuesList(location[0], location[1], location[2], self.deltaScaleCore), joint=nurbs)
        newTime = 0
        for key, nurbsList in clipsDictRot["arms"].items():
            newTime += 1
            for nurbs, location in nurbsList.items():
                Clips().PosesRotate(startTime=newTime, endtime=newTime,
                                       value=valuesList(location[0], location[1], location[2], self.deltaScaleArms), joint=nurbs)
        newTime = 0
        for key, nurbsList in clipsDictRot["legs"].items():
            newTime += 1
            for nurbs, location in nurbsList.items():
                Clips().PosesRotate(startTime=newTime, endtime=newTime,
                                       value=valuesList(location[0], location[1], location[2], self.deltaScaleLegs), joint=nurbs)
        newTime = 0
        for key, nurbsList in clipsDictRot["core"].items():
            newTime += 1
            for nurbs, location in nurbsList.items():
                Clips().PosesRotate(startTime=newTime, endtime=newTime,
                                       value=valuesList(location[0], location[1], location[2], self.deltaScaleCore), joint=nurbs)

class Clips:
    def PosesTranslate(self, startTime, endtime, joint, value):
        cmds.setKeyframe(joint, attribute='translateX', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[0])
        cmds.setKeyframe(joint, attribute='translateY', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[1])
        cmds.setKeyframe(joint, attribute='translateZ', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[2])
        return startTime + 2

    def PosesRotate(self, startTime, endtime, joint, value):
        cmds.setKeyframe(joint, attribute='rotateX', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[0])
        cmds.setKeyframe(joint, attribute='rotateY', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[1])
        cmds.setKeyframe(joint, attribute='rotateZ', t=(Frames().calcFrames()[startTime], Frames().calcFrames()[endtime]), v=value[2])
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
