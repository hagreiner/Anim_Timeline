import maya.cmds as cmds
from constants import MAX_TIME, MIN_TIME
from timeLine import CreateBuild, Play
from functools import partial
import edgeLoops
import logPoses


def start():
    cmds.currentUnit(time='ntsc')
    reset()
    MainMenu().start()


def end():
    reset()
    cmds.select(all=True)
    cmds.delete()
    if cmds.window("window", exists=True):
        cmds.deleteUI("window", window=True)


def delete():
    cmds.select(all=True)
    cmds.delete()


class MainMenu:
    def __init__(self):
        self.col = "mainCol"
        self.window = "mainUI"
        self.width = 300
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.window = cmds.window(self.window, title="Animation Timeline",
                                  minimizeButton=False, maximizeButton=False, sizeable=False)

    def start(self):
        self.typeCol = cmds.columnLayout(self.col, parent=self.window, w=self.width)

        # section one
        frameLayout1 = cmds.frameLayout(width=self.width, label="Skeleton Creation", collapse=True, collapsable=True, marginHeight=10,
                                        marginWidth=5, parent=self.typeCol, ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.text("Center Joints", bgc=(0.5, 0.5, 0.5), h=20)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 10) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Center", command=lambda args: edgeLoops.AssignSelection().logSelect("Center"), height=20)
        cmds.textField("Center", en=False, text="None", height=20)
        cmds.button(label="Neck", command=lambda args: edgeLoops.AssignSelection().logSelect("Neck"), height=20)
        cmds.textField("Neck", en=False, text="None", height=20)
        cmds.button(label="Top Spine Joint", command=lambda args: edgeLoops.AssignSelection().logSelect("Top_Spine_Joint"), height=20)
        cmds.textField("Top Spine_Joint", en=False, text="None", height=20)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.text("Left Joints", bgc=(0.5, 0.5, 0.5), h=20)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 10) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Left Hip", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Hip"), height=20)
        cmds.textField("Left_Hip", en=False, text="None", height=20)
        cmds.button(label="Left Knee", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Knee"), height=20)
        cmds.textField("Left_Knee", en=False, text="None", height=20)
        cmds.button(label="Left Foot", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Foot"), height=20)
        cmds.textField("Left_Foot", en=False, text="None", height=20)
        cmds.button(label="Left Foot Flex", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Foot_Flex"), height=20)
        cmds.textField("Left_Foot_Flex", en=False, text="None", height=20)
        cmds.button(label="Left Toe", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Toe"), height=20)
        cmds.textField("Left_Toe", en=False, text="None", height=20)
        cmds.button(label="Left Shoulder Blade", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Shoulder_Blade"), height=20)
        cmds.textField("Left_Shoulder_Blade", en=False, text="None", height=20)
        cmds.button(label="Left Shoulder", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Shoulder"), height=20)
        cmds.textField("Left_Shoulder", en=False, text="None", height=20)
        cmds.button(label="Left Elbow", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Elbow"), height=20)
        cmds.textField("Left_Elbow", en=False, text="None", height=20)
        cmds.button(label="Left Lower Arm Rotate", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Lower_Arm_Rotate"), height=20)
        cmds.textField("Left_Lower_Arm_Rotate", en=False, text="None", height=20)
        cmds.button(label="Left Wrist", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Wrist"), height=20)
        cmds.textField("Left_Wrist", en=False, text="None", height=20)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.text("Right Joints", bgc=(0.5, 0.5, 0.5), h=20)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 10) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Right Hip", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Hip"), height=20)
        cmds.textField("Right_Hip", en=False, text="None", height=20)
        cmds.button(label="Right Knee", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Knee"), height=20)
        cmds.textField("Right_Knee", en=False, text="None", height=20)
        cmds.button(label="Right Foot", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Foot"), height=20)
        cmds.textField("Right_Foot", en=False, text="None", height=20)
        cmds.button(label="Right Foot Flex", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Foot_Flex"), height=20)
        cmds.textField("Right_Foot_Flex", en=False, text="None", height=20)
        cmds.button(label="Right Toe", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Toe"), height=20)
        cmds.textField("Right_Toe", en=False, text="None", height=20)
        cmds.button(label="Right Shoulder Blade", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Shoulder_Blade"), height=20)
        cmds.textField("Right_Shoulder_Blade", en=False, text="None", height=20)
        cmds.button(label="Right Shoulder", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Shoulder"), height=20)
        cmds.textField("Right_Shoulder", en=False, text="None", height=20)
        cmds.button(label="Right Elbow", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Elbow"), height=20)
        cmds.textField("Right_Elbow", en=False, text="None", height=20)
        cmds.button(label="Right Lower Arm Rotate", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Lower_Arm_Rotate"), height=20)
        cmds.textField("Right_Lower_Arm_Rotate", en=False, text="None", height=20)
        cmds.button(label="Right Wrist", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Wrist"), height=20)
        cmds.textField("Right_Wrist", en=False, text="None", height=20)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Confirm", command=lambda args: edgeLoops.LogLoops().convertToJoint())
        cmds.text("", h=1)
        cmds.button(label="Create Hierarchy",
                    command=lambda args: (edgeLoops.LinkBones().createChildren(), edgeLoops.LinkBones().createIK()))

        cmds.text("\n", height=5)
        cmds.separator()
        cmds.text(" ")

        cmds.button(label="About this Tool", command=lambda args: InfoWindow(type="skeletonCreation").create())
        # cmds.text("- select faces, vertices, or edges the correspond with the joint type", align="left")

        # section two
        frameLayout1 = cmds.frameLayout(width=self.width, label="Log Poses", collapse=True, collapsable=True, marginHeight=10,
                                        marginWidth=5, parent=self.typeCol, ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, (self.width - 10)/2.0), (2, (self.width - 10)/2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Pose One", command=lambda args: logPoses.findPoseInformation().savePose("Pose_One"), height=20)
        cmds.textField("Pose_One", en=False, text="None", height=20)
        cmds.button(label="Pose Two", command=lambda args: logPoses.findPoseInformation().savePose("Pose_Two"), height=20)
        cmds.textField("Pose_Two", en=False, text="None", height=20)
        cmds.button(label="Pose Three", command=lambda args: logPoses.findPoseInformation().savePose("Pose_Three"), height=20)
        cmds.textField("Pose_Three", en=False, text="None", height=20)
        cmds.button(label="Pose Four", command=lambda args: logPoses.findPoseInformation().savePose("Pose_Four"), height=20)
        cmds.textField("Pose_Four", en=False, text="None", height=20)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Confirm All Poses", command=lambda args: (CreateBuild().moveCurves()))

        cmds.text("", h=5)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 20) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.text("Pose One Length")
        cmds.intSlider("Pose_One_Length", min=0, max=5, value=0)
        cmds.text("Pose Two Length")
        cmds.intSlider("Pose_Two_Length", min=0, max=5, value=0)
        cmds.text("Pose Three Length")
        cmds.intSlider("Pose_Three_Length", min=0, max=5, value=0)
        cmds.text("Pose Four Length")
        cmds.intSlider("Pose_Four_Length", min=0, max=5, value=0)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Animate Cycle", command=lambda args: Play().forwardsRig())
        cmds.button(label="Stop", command=lambda args: Play().stop())
        cmds.button(label="Reset", command=lambda args: logPoses.Reset().resetPosesAndUI())

        cmds.text("\n", height=5)
        cmds.separator()
        cmds.text(" ")

        cmds.text("words about this")

        # section three
        frameLayout1 = cmds.frameLayout(width=self.width, label="Preset Animations", collapse=True, collapsable=True, marginHeight=10,
                                        marginWidth=5, parent=self.typeCol, ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width-10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.radioCollection('placingRadioCollection')
        cmds.radioButton('default', label='Default Cycle', sl=True)

        cmds.floatSliderGrp('deltaScaleArms', label='Arms Scale', field=True, minValue=0, maxValue=1,
                            value=1, columnWidth=[(1, 125), (2, 25), (3, self.width - 150)], cal=[1, "center"])
        cmds.floatSliderGrp('deltaScaleLegs', label='Legs Scale', field=True, minValue=0, maxValue=1,
                            value=1, columnWidth=[(1, 125), (2, 25), (3, self.width - 150)], cal=[1, "center"])
        cmds.floatSliderGrp('deltaScaleCore', label='Core Scale', field=True, minValue=0, maxValue=1,
                            value=1, columnWidth=[(1, 125), (2, 25), (3, self.width - 150)], cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Animate", command=lambda args: Play().forwardsPreSetClip())
        cmds.button(label="Stop", command=lambda args: Play().stop())
        cmds.button(label="Reset", command=lambda args: logPoses.Reset().resetRig())

        frameLayout1 = cmds.frameLayout(width=self.width, label="Timeline Length", collapse=False, collapsable=True,
                                        marginHeight=10,
                                        marginWidth=5, parent=self.typeCol,
                                        ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 20) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.text("Animation Length")
        cmds.intSlider("frameNum", min=MIN_TIME, max=MAX_TIME, value=(MIN_TIME + MAX_TIME) / 10.0)

        #put this at end
        winHeight = 0
        for child in cmds.columnLayout(self.typeCol, q=1, ca=1):
            winHeight += eval('cmds.' + cmds.objectTypeUI(child) + '("' + child + '", q=1, h=1)')
        cmds.window(self.window, e=1, h=winHeight)
        cmds.showWindow(self.window)


class InfoWindow:
    def __init__(self, type):
        self.type = type
        self.col = "helpCol"
        self.window = "helpUI"
        self.width = 500

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.window = cmds.window(self.window, title="Information",
                                  minimizeButton=False, maximizeButton=False, sizeable=False)

        if type == "skeletonCreation":
            self.informationList = rigHelp()

    def create(self):
        cmds.columnLayout(self.col, parent=self.window)
        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.col)
        cmds.text("About:", height=30)
        for textLine in self.informationList:
            cmds.text(textLine, align="left")

        cmds.text("\n", height=5)
        cmds.separator()
        cmds.text(" ")

        cmds.rowColumnLayout(numberOfColumns=3,
                             columnWidth=[(1, self.width/3.0), (2, self.width/3.0), (3, self.width/3.0)], parent=self.col)
        cmds.text("")
        cmds.button(label="Okay", command=lambda args: InfoWindow(type=self.type).destroy())

        cmds.rowColumnLayout(numberOfColumns=3,
                             columnWidth=[(1, self.width / 3.0), (2, self.width / 3.0), (3, self.width / 3.0)],
                             parent=self.col)
        cmds.text("")

        # end line
        cmds.showWindow(self.window)

    def destroy(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)


def reset():
    cmds.currentTime(0, edit=True)


def frameCollapseChanged(mainLayout):
    cmds.evalDeferred(
        "cmds.window('mainUI', e=1, h=sum([eval('cmds.' + cmds.objectTypeUI(child) + '(\\'' + child + '\\', q=1, h=1)') "
        "for child in cmds.columnLayout('" + mainLayout + "', q=1, ca=1)]))")


def rigHelp():
    return [
        " - select faces, vertices, or edges the correspond with the joint type",
        " - press the button for the joint to assign it to a position",
        " - pressing the first button will place the joints in world space",
        " - pressing the second button will connect the joints and create basic ik with handles",
        " - included ik handles are: arm movement, arm rotation, leg movement, and foot controls",
    ]

