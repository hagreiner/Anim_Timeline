import maya.cmds as cmds
from constants import MAX_TIME, MIN_TIME
import logPoses
import poseLibrary


class LoadCurves:
    userCurves = None

    def add(self):
        LoadCurves.userCurves = cmds.ls(sl=True)


class LoadPoseData:
    def findPoseInformation(self):
        pass


class CreateBuild:
    curvesLocationDict = None
    curvesRotationDict = None

    def moveCurves(self):
        """
        :summary: creates class variables for dictionaries from the the pose data created by user nurb movement
        :parameter: none
        :return: nothing
        """
        CreateBuild.curvesLocationDict = logPoses.findPoseInformation.PosesDictMove
        CreateBuild.curvesRotationDict = logPoses.findPoseInformation.PosesDictRot


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

        self.default = cmds.radioButton('default', query=True, select=True)

    def forwardsRig(self):
        """
        :summary: rests all the data for the user data animations, resets the timeline length, resets the data, and plays the clip
        :return: nothing
        """
        Frames.frameCount = 5 + self.PoseOneScale + self.PoseTwoScale + self.PoseThreeScale + self.PoseFourScale
        Play().stop()
        cmds.playbackOptions(minTime='0sec', maxTime=str(Frames.frameCount/30.0) + 'sec')
        LoadClips().loadRig()
        LoadClips().runRig()
        cmds.play(forward=True)

    def forwardsPreSetClip(self):
        """
        :summary: rests all the data for the ik data animations, resets the timeline length, resets the data, and plays the clip
        :return: nothing
        """
        clip_move, clip_rot = LoadClips().loadPreSet()
        Frames.frameCount = len(clip_move["arms"].keys()) + 1
        Play().stop()
        cmds.playbackOptions(minTime='0sec', maxTime=str(Frames.frameCount / 30.0) + 'sec')
        LoadClips().runPreSet(clipsDictMove=clip_move, clipsDictRot=clip_rot)
        cmds.play(forward=True)

    def stop(self):
        """
        :summary: stops the time slider
        :return: nothing
        """
        cmds.play(state=False)


class LoadClips(Play):
    def loadRig(self):
        """
        :summary: collects the user created pose data formatted from another script and separates it out into separate dictionaries
        :return: nothing
        """
        LoadClips.PoseOneTranslate = CreateBuild.curvesLocationDict["Pose_One"]
        LoadClips.PoseTwoTranslate = CreateBuild.curvesLocationDict["Pose_Two"]
        LoadClips.PoseThreeTranslate = CreateBuild.curvesLocationDict["Pose_Three"]
        LoadClips.PoseFourTranslate = CreateBuild.curvesLocationDict["Pose_Four"]

        LoadClips.PoseOneRotation = CreateBuild.curvesLocationDict["Pose_One"]
        LoadClips.PoseTwoRotation = CreateBuild.curvesLocationDict["Pose_Two"]
        LoadClips.PoseThreeRotation = CreateBuild.curvesLocationDict["Pose_Three"]
        LoadClips.PoseFourRotation = CreateBuild.curvesLocationDict["Pose_Four"]

    def runRig(self):
        """
        :summary: takes the user data collected from the nurbs handles and puts in on the timeline
        :parameter: none
        :return: nothing
        """
        newTime = 1
        for nurbs, location in LoadClips.PoseOneTranslate.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseOneScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseOneScale)
        for nurbs, location in LoadClips.PoseTwoTranslate.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseTwoScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseTwoScale)
        for nurbs, location in LoadClips.PoseThreeTranslate.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseThreeScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseThreeScale)
        for nurbs, location in LoadClips.PoseFourTranslate.items():
            Clips().PosesTranslate(startTime=newTime, endtime=newTime + self.PoseFourScale, value=location, joint=nurbs)

        newTime = 1
        for nurbs, location in LoadClips.PoseOneRotation.items():
            Clips().PosesRotate(startTime=newTime, endtime=newTime + self.PoseOneScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseOneScale)
        for nurbs, location in LoadClips.PoseTwoRotation.items():
            Clips().PosesRotate(startTime=newTime, endtime=newTime + self.PoseTwoScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseTwoScale)
        for nurbs, location in LoadClips.PoseThreeRotation.items():
            Clips().PosesRotate(startTime=newTime, endtime=newTime + self.PoseThreeScale, value=location, joint=nurbs)
        newTime += (1 + self.PoseThreeScale)
        for nurbs, location in LoadClips.PoseFourRotation.items():
            Clips().PosesRotate(startTime=newTime, endtime=newTime + self.PoseFourScale, value=location, joint=nurbs)

    def loadPreSet(self):
        """
        :summary: depending on the boolean a function returning pose data is chosen
        :parameter: none
        :return: dictionaries of translation and rotation data
        """
        if self.default == True:
            return poseLibrary.default()

    def runPreSet(self, clipsDictMove, clipsDictRot):
        """
        :summary: load clips on the timeline from ik data
        :param clipsDictMove: a dictionary of all the translation data for all the poses for all the nurbs handles
        :param clipsDictRot: a dictionary of all the rotation data for all the poses for all the nurbs handles
        :return: nothing
        """
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
    """
    :summary: created keyed from on the timeline for rotation or translation
    :param startTime: what time the pose should start
    :param endtime: what time the pose should end
    :param joint: the joint (or nurbs handle or ik handle) that is being moved or rotated
    :param value: a list of x, y, z values in the pose of "joint"
    :return: a time for the next pose (not always needed)
    """
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
    """
    :summary: sets the time slider on the timeline to 0
    :parameter: none
    :return: nothing
    """
    cmds.currentTime(0, edit=True)


class Frames:
    """
    :summary: converts the amount of frames needed into units of time based on the number of frames on the timeline
    :parameter: none
    :return: a list of frames
    """
    frameCount = MIN_TIME

    def calcFrames(self):
        returnList = []
        for x in range(Frames.frameCount):
            returnList.append((Play.frameNum/Frames.frameCount)*x)
        return returnList


def valuesList(X, Y, Z, percent):
    """
    :param X: x translation or rotation
    :param Y: y translation or rotation
    :param Z: z translation or rotation
    :param percent: scale value
    :return: list of the new x, y, z coordinates with the scale applied
    """
    return [(X*percent), (Y*percent), (Z*percent)]


class RotatePos:
    """
    :summary: rotates an object around a point and converts that matrix into x, y, z values
    :param x: x rotation value
    :param y: y rotation value
    :param z: z rotation value
    :param object: the object to be rotated
    :param parent: the parent x, y, z position
    """
    def __init__(self, x, y, z, object, parent):
        #self.parent = {"posX": 0, "posY": 0, "posZ": 0,}
        self.parent = parent
        self.object = object
        self.rotX = x
        self.rotY = y
        self.rotZ = z

    def xformRot(self):
        cmds.rotate(self.rotX, self.rotY, self.rotZ, self.object,
                    pivot=(self.parent["posX"], self.parent["posY"], self.parent["posZ"]))
        location = cmds.xform(self.object, query=True, bb=True)
        cmds.rotate(0, 0, 0, self.object, pivot=(self.parent["posX"], self.parent["posY"], self.parent["posZ"]))

        return [(location[0] + location[3])/2.0, (location[1] + location[4])/2.0, (location[2] + location[5])/2.0]
