import maya.cmds as cmds


class findPoseInformation:
    PosesDict = {}

    def savePose(self, strType):
        nurbsList = [
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
        nurbsDict = {}
        for nurbs in nurbsList:
            nurbsDict[nurbs] = transforms(nurbs)

        findPoseInformation.PosesDict[strType] = nurbsDict
        cmds.textField(strType, edit=True, text="Pose Confirmed")


def transforms(selection):
    return cmds.xform(selection, query=True, translation=True)
