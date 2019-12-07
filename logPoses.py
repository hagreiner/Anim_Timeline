import maya.cmds as cmds


class findPoseInformation:
    PosesDict = {}

    def __init__(self):
        self.nurbsList = [
            "circle_Right_Foot",
            "circle_Right_Leg",
            "circle_Left_Foot",
            "circle_Left_Leg",
            "circle_Right_Arm",
            "circle_Right_Arm_Rot",
            "circle_Left_Arm",
            "circle_Left_Arm_Rot",
            "circle_Center_Bend",
        ]
        self.Poses = ["Pose_One", "Pose_Two", "Pose_Three", "Pose_Four"]

    def savePose(self, strType):
        nurbsDict = {}
        for nurbs in self.nurbsList:
            nurbsDict[nurbs] = transforms(nurbs)

        findPoseInformation.PosesDict[strType] = nurbsDict
        cmds.textField(strType, edit=True, text="Pose Confirmed")


def transforms(selection):
    return cmds.xform(selection, query=True, translation=True)


class Reset(findPoseInformation):
    def resetPosesAndUI(self):
        findPoseInformation.PosesDict = {}
        for nurbs in self.nurbsList:
            cmds.move(0, 0, 0, nurbs)
        for pose in self.Poses:
            cmds.textField(pose, edit=True, text="None")