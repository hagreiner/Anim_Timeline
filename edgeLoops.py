import maya.cmds as cmds

class AssignSelection:
    def logSelect(self, strType):
        selection = cmds.ls(sl=True)
        LogLoops.LoopsDict[strType] = selection
        cmds.textField(strType, edit=True, text=selection[0])


class LogLoops:
    LoopsDict = {
        "Center": None,
        "Neck": None,
        "Top_Spine_Joint": None,

        "Left_Hip": None,
        "Left_Knee": None,
        "Left_Foot": None,
        "Left_Foot_Flex": None,
        "Left_Toe": None,
        "Left_Shoulder_Blade": None,
        "Left_Shoulder": None,
        "Left_Elbow": None,
        "Left_Lower_Arm_Rotate": None,
        "Left_Wrist": None,

        "Right_Hip": None,
        "Right_Knee": None,
        "Right_Foot": None,
        "Right_Foot_Flex": None,
        "Right_Toe": None,
        "Right_Shoulder_Blade": None,
        "Right_Shoulder": None,
        "Right_Elbow": None,
        "Right_Lower_Arm_Rotate": None,
        "Right_Wrist": None,
    }
    def convertToJoint(self):
        for name, points in LogLoops.LoopsDict.items():
            position = CreateJoint().addOne(points)
            CreateJoint.jointDict[name] = position
        print(CreateJoint.jointDict)


class CreateJoint:
    jointDict = {}

    def addOne(self, selection):
        location = averageLocation(selection)
        cmds.select(clear=True)
        return cmds.joint(p=(location[0], location[1], location[2]))


def averageLocation(selection):
    averagedList = []

    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, query=True)

    averagedList.append(((xmin + xmax)/2.0))
    averagedList.append(((ymin + ymax)/2.0))
    averagedList.append(((zmin + zmax)/2.0))

    return averagedList


class LinkBones:
    """
    "Center": None,
        "Neck": None,
        "Top_Spine_Joint": None,

        "Left_Hip": None,
        "Left_Knee": None,
        "Left_Foot": None,
        "Left_Foot_Flex": None,
        "Left_Toe": None,
        
        "Left_Shoulder_Blade": None,
        "Left_Shoulder": None,
        "Left_Elbow": None,
        "Left_Lower_Arm_Rotate": None,
        "Left_Wrist": None,

        "Right_Hip": None,
        "Right_Knee": None,
        "Right_Foot": None,
        "Right_Foot_Flex": None,
        "Right_Toe": None,
        "Right_Shoulder_Blade": None,
        "Right_Shoulder": None,
        "Right_Elbow": None,
        "Right_Lower_Arm_Rotate": None,
        "Right_Wrist": None,
    """
    def createChildren(self):
        cmds.parent(CreateJoint.jointDict["Top_Spine_Joint"], CreateJoint.jointDict["Center"])
        cmds.parent(CreateJoint.jointDict["Neck"], CreateJoint.jointDict["Top_Spine_Joint"])
        cmds.parent(CreateJoint.jointDict["Left_Hip"], CreateJoint.jointDict["Center"])
        cmds.parent(CreateJoint.jointDict["Right_Hip"], CreateJoint.jointDict["Center"])

        cmds.parent(CreateJoint.jointDict["Left_Knee"], CreateJoint.jointDict["Left_Hip"])
        cmds.parent(CreateJoint.jointDict["Left_Foot"], CreateJoint.jointDict["Left_Knee"])
        cmds.parent(CreateJoint.jointDict["Left_Foot_Flex"], CreateJoint.jointDict["Left_Foot"])
        cmds.parent(CreateJoint.jointDict["Left_Toe"], CreateJoint.jointDict["Left_Foot_Flex"])

        cmds.parent(CreateJoint.jointDict["Right_Knee"], CreateJoint.jointDict["Right_Hip"])
        cmds.parent(CreateJoint.jointDict["Right_Foot"], CreateJoint.jointDict["Right_Knee"])
        cmds.parent(CreateJoint.jointDict["Right_Foot_Flex"], CreateJoint.jointDict["Right_Foot"])
        cmds.parent(CreateJoint.jointDict["Right_Toe"], CreateJoint.jointDict["Right_Foot_Flex"])

        cmds.parent(CreateJoint.jointDict["Left_Shoulder_Blade"], CreateJoint.jointDict["Top_Spine_Joint"])
        cmds.parent(CreateJoint.jointDict["Left_Shoulder"], CreateJoint.jointDict["Left_Shoulder_Blade"])
        cmds.parent(CreateJoint.jointDict["Left_Elbow"], CreateJoint.jointDict["Left_Shoulder"])
        cmds.parent(CreateJoint.jointDict["Left_Lower_Arm_Rotate"], CreateJoint.jointDict["Left_Elbow"])
        cmds.parent(CreateJoint.jointDict["Left_Wrist"], CreateJoint.jointDict["Left_Lower_Arm_Rotate"])

        cmds.parent(CreateJoint.jointDict["Right_Shoulder_Blade"], CreateJoint.jointDict["Top_Spine_Joint"])
        cmds.parent(CreateJoint.jointDict["Right_Shoulder"], CreateJoint.jointDict["Right_Shoulder_Blade"])
        cmds.parent(CreateJoint.jointDict["Right_Elbow"], CreateJoint.jointDict["Right_Shoulder"])
        cmds.parent(CreateJoint.jointDict["Right_Lower_Arm_Rotate"], CreateJoint.jointDict["Right_Elbow"])
        cmds.parent(CreateJoint.jointDict["Right_Wrist"], CreateJoint.jointDict["Right_Lower_Arm_Rotate"])

    def createIK(self):
        pass