import maya.cmds as cmds


class findPoseInformation:
    PosesDictMove = {}
    PosesDictRot = {}

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
        """
        :summary: adds pose information in the form of a dictionary to the PosesDictMove and PoseDictRot
        :param strType: the name of the pose
        :return: nothing
        """
        nurbsMoveDict = {}
        for nurbs in self.nurbsList:
            nurbsMoveDict[nurbs] = transforms(nurbs)

        nurbsRotDict = {}
        for nurbs in self.nurbsList:
            nurbsRotDict[nurbs] = rotations(nurbs)

        findPoseInformation.PosesDictRot[strType] = nurbsRotDict
        findPoseInformation.PosesDictMove[strType] = nurbsMoveDict
        cmds.textField(strType, edit=True, text="Pose Confirmed")


def transforms(selection):
    """
    :summary: queries the tranforms of selection
    :param selection: a nurbs item
    :return: the transforms in x, y, z format
    """
    return cmds.xform(selection, query=True, translation=True)


def rotations(selection):
    """
    :summary: queries the rotations of selection
    :param selection: a nurbs item
    :return: the rotation in x, y, z format
    """
    return cmds.xform(selection, query=True, rotation=True)


class Reset(findPoseInformation):
    """
    :summary: rests the nurb to 0, 0, 0 and clears the UI
    :return: nothing
    """
    def resetPosesAndUI(self):
        findPoseInformation.PosesDict = {}
        for nurbs in self.nurbsList:
            cmds.move(0, 0, 0, nurbs)
            cmds.rotate(0, 0, 0, nurbs)
        for pose in self.Poses:
            cmds.textField(pose, edit=True, text="None")

    def resetRig(self):
        for nurbs in self.nurbsList:
            cmds.move(0, 0, 0, nurbs)
            cmds.rotate(0, 0, 0, nurbs)
