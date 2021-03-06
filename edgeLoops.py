import maya.cmds as cmds
import ikCreation


class AssignSelection:
    def logSelect(self, strType):
        """
        :summary: updates the LogLoops.LoopsDict with the selection
        :param strType: a string that has the same name as the joint and textbox
        :return: nothing
        """
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
        """
        :summary: converts the selections in the LoopsDict to world space positions and joints
        :parameter: none
        :return: nothing
        """
        for name, points in LogLoops.LoopsDict.items():
            position = CreateJoint().addOne(points)
            CreateJoint.jointDict[name] = position


class CreateJoint:
    jointDict = {}

    def addOne(self, selection):
        """
        :summary: joints are created based a selected area
        :param selection: a place on an object
        :return: a joint
        """
        location = averageLocation(selection)
        cmds.select(clear=True)
        return cmds.joint(p=(location[0], location[1], location[2]))


def averageLocation(selection):
    """
    :summary: finds the world space matrix and converts it to x, y, z position
    :param selection: the object to find the bounding box of
    :return: x, y, z position list
    """
    averagedList = []

    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, query=True)

    averagedList.append(((xmin + xmax)/2.0))
    averagedList.append(((ymin + ymax)/2.0))
    averagedList.append(((zmin + zmax)/2.0))

    return averagedList


class LinkBones:
    def createChildren(self):
        """
        :summary: creates a hierarchy on the joints
        :return: nothing
        """
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
        """
        :summary: creates the ik and nurbs handles based on the joints in the CreateJoint.jointDict dictionary
        :parameter: none
        :return: all the created nurbs handles
        """
        # right leg
        rightLegPos = averageLocation(LogLoops.LoopsDict["Right_Foot"])
        rightToePos = averageLocation(LogLoops.LoopsDict["Right_Toe"])
        addedRightLegPos = averageLocation(LogLoops.LoopsDict["Right_Knee"])

        ikCreation.createHandle(CreateJoint.jointDict["Right_Foot"], CreateJoint.jointDict["Right_Toe"], name="Right_Foot")
        rightFoot = ikCreation.createNurbsHandle(rightToePos, [5, 5, 5],  [0, 0, 0], "Right_Foot",
            listAdd(rightToePos, [0, 0, 0]), True)

        ikCreation.createHandle(CreateJoint.jointDict["Right_Hip"], CreateJoint.jointDict["Right_Foot"], name="Right_Leg")
        rightLeg = ikCreation.createNurbsHandle(rightLegPos, [10, 20, 5],  [90, 0, 0], "Right_Leg",
            listAdd(listSubtract(addedRightLegPos, rightLegPos), [0, 0, 15]), True)

        cmds.parent(rightFoot, rightLeg)

        # left leg
        leftLegPos = averageLocation(LogLoops.LoopsDict["Left_Foot"])
        leftToePos = averageLocation(LogLoops.LoopsDict["Left_Toe"])
        addedLeftLegPos = averageLocation(LogLoops.LoopsDict["Left_Knee"])

        ikCreation.createHandle(CreateJoint.jointDict["Left_Foot"], CreateJoint.jointDict["Left_Toe"], name="Left_Foot")
        leftFoot = ikCreation.createNurbsHandle(leftToePos, [5, 5, 5],  [0, 0, 0], "Left_Foot",
            listAdd(leftToePos, [0, 0, 0]), True)

        ikCreation.createHandle(CreateJoint.jointDict["Left_Hip"], CreateJoint.jointDict["Left_Foot"], name="Left_Leg")
        leftLeg = ikCreation.createNurbsHandle(leftLegPos, [10, 20, 5],  [90, 0, 0], "Left_Leg",
            listAdd(listSubtract(addedLeftLegPos, leftLegPos), [0, 0, 15]), True)

        cmds.parent(leftFoot, leftLeg)

        # right arm
        rightWristPos = averageLocation(LogLoops.LoopsDict["Right_Wrist"])
        addedRightElbow = averageLocation(LogLoops.LoopsDict["Right_Elbow"])
        rightArmRot = averageLocation(LogLoops.LoopsDict["Right_Lower_Arm_Rotate"])

        ikCreation.createHandle(CreateJoint.jointDict["Right_Shoulder"], CreateJoint.jointDict["Right_Wrist"], name="Right_Arm")
        rightArm = ikCreation.createNurbsHandle(rightWristPos, [10, 10, 10],  [0, 90, 0], "Right_Arm",
            listAdd(listSubtract(addedRightElbow, rightWristPos), [0, 0, -15]), True)

        ikCreation.createHandle(CreateJoint.jointDict["Right_Elbow"], CreateJoint.jointDict["Right_Lower_Arm_Rotate"], name="Right_Arm_Rot")
        rightArm_rotate = ikCreation.createNurbsHandle(rightArmRot, [10, 10, 10],  [0, 90, 0], "Right_Arm_Rot",
           [0, 0, 0], True)

        cmds.parent(rightArm_rotate, rightArm)

        # left arm
        leftWristPos = averageLocation(LogLoops.LoopsDict["Left_Wrist"])
        addedLeftElbow = averageLocation(LogLoops.LoopsDict["Left_Elbow"])
        leftArmRot = averageLocation(LogLoops.LoopsDict["Left_Lower_Arm_Rotate"])

        ikCreation.createHandle(CreateJoint.jointDict["Left_Shoulder"], CreateJoint.jointDict["Left_Wrist"], name="Left_Arm")
        leftArm = ikCreation.createNurbsHandle(leftWristPos, [10, 10, 10],  [0, 90, 0], "Left_Arm",
            listAdd(listSubtract(addedLeftElbow, leftWristPos), [0, 0, -15]), True)

        ikCreation.createHandle(CreateJoint.jointDict["Left_Elbow"], CreateJoint.jointDict["Left_Lower_Arm_Rotate"], name="Left_Arm_Rot")
        leftArm_rotate = ikCreation.createNurbsHandle(leftArmRot, [10, 10, 10],  [0, 90, 0], "Left_Arm_Rot",
           [0, 0, 0], True)

        cmds.parent(leftArm_rotate, leftArm)

        # center
        center = averageLocation(LogLoops.LoopsDict["Center"])
        spineJoint = averageLocation(LogLoops.LoopsDict["Top_Spine_Joint"])

        ikCreation.createHandle(CreateJoint.jointDict["Center"], CreateJoint.jointDict["Top_Spine_Joint"], name="Center_Bend")
        centerRot = ikCreation.createNurbsHandle(center, [25, 25, 25], [90, 0, 0], "Center_Bend",
                                                 [0, 0, 0], True) #listAdd(listSubtract(spineJoint, center), center)

        # return
        return rightArm, leftArm, leftLeg, rightLeg, leftArm_rotate, rightArm_rotate, rightFoot, leftFoot, centerRot


def listSubtract(listOne, listTwo):
    """
    :summary: subtracts the items in a len(3) list from another len(3) list
    :param listOne: larger list
    :param listTwo: smaller list
    :return: returns the subtracted result
    """
    return [(listOne[0] - listTwo[0]), (listOne[1] - listTwo[1]), (listOne[2] - listTwo[2])]


def listAdd(listOne, listTwo):
    """
    :summary: adds the items of two len(3) lists together
    :param listOne: a three item list
    :param listTwo: a three item list
    :return: the result of the lists
    """
    return [(listOne[0] + listTwo[0]), (listOne[1] + listTwo[1]), (listOne[2] + listTwo[2])]
