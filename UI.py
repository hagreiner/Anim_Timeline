import maya.cmds as cmds
from constants import WIDTH, MAX_TIME, MIN_TIME
from timeLine import CreateBuild, Play
from functools import partial
import edgeLoops


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
        cmds.button(label="Center", command=lambda args: edgeLoops.AssignSelection().logSelect("Center"))
        cmds.textField("Center", en=False, text="None")
        cmds.button(label="Neck", command=lambda args: edgeLoops.AssignSelection().logSelect("Neck"))
        cmds.textField("Neck", en=False, text="None")
        cmds.button(label="Top Spine Joint", command=lambda args: edgeLoops.AssignSelection().logSelect("Top_Spine_Joint"))
        cmds.textField("Top Spine_Joint", en=False, text="None")

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.text("Left Joints", bgc=(0.5, 0.5, 0.5), h=20)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 10) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Left Hip", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Hip"))
        cmds.textField("Left_Hip", en=False, text="None")
        cmds.button(label="Left Knee", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Knee"))
        cmds.textField("Left_Knee", en=False, text="None")
        cmds.button(label="Left Foot", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Foot"))
        cmds.textField("Left_Foot", en=False, text="None")
        cmds.button(label="Left Foot Flex", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Foot_Flex"))
        cmds.textField("Left_Foot_Flex", en=False, text="None")
        cmds.button(label="Left Toe", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Toe"))
        cmds.textField("Left_Toe", en=False, text="None")
        cmds.button(label="Left Shoulder Blade", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Shoulder_Blade"))
        cmds.textField("Left_Shoulder_Blade", en=False, text="None")
        cmds.button(label="Left Shoulder", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Shoulder"))
        cmds.textField("Left_Shoulder", en=False, text="None")
        cmds.button(label="Left Elbow", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Elbow"))
        cmds.textField("Left_Elbow", en=False, text="None")
        cmds.button(label="Left Lower Arm Rotate", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Lower_Arm_Rotate"))
        cmds.textField("Left_Lower_Arm_Rotate", en=False, text="None")
        cmds.button(label="Left Wrist", command=lambda args: edgeLoops.AssignSelection().logSelect("Left_Wrist"))
        cmds.textField("Left_Wrist", en=False, text="None")

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.text("Right Joints", bgc=(0.5, 0.5, 0.5), h=20)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 10) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Right Hip", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Hip"))
        cmds.textField("Right_Hip", en=False, text="None")
        cmds.button(label="Right Knee", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Knee"))
        cmds.textField("Right_Knee", en=False, text="None")
        cmds.button(label="Right Foot", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Foot"))
        cmds.textField("Right_Foot", en=False, text="None")
        cmds.button(label="Right Foot Flex", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Foot_Flex"))
        cmds.textField("Right_Foot_Flex", en=False, text="None")
        cmds.button(label="Right Toe", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Toe"))
        cmds.textField("Right_Toe", en=False, text="None")
        cmds.button(label="Right Shoulder Blade", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Shoulder_Blade"))
        cmds.textField("Right_Shoulder_Blade", en=False, text="None")
        cmds.button(label="Right Shoulder", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Shoulder"))
        cmds.textField("Right_Shoulder", en=False, text="None")
        cmds.button(label="Right Elbow", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Elbow"))
        cmds.textField("Right_Elbow", en=False, text="None")
        cmds.button(label="Right Lower Arm Rotate", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Lower_Arm_Rotate"))
        cmds.textField("Right_Lower_Arm_Rotate", en=False, text="None")
        cmds.button(label="Right Wrist", command=lambda args: edgeLoops.AssignSelection().logSelect("Right_Wrist"))
        cmds.textField("Right_Wrist", en=False, text="None")

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Confirm", command=lambda args: edgeLoops.LogLoops().convertToJoint())
        cmds.button(label="Create Hierarchy",
                    command=lambda args: (edgeLoops.LinkBones().createChildren(), edgeLoops.LinkBones().createIK()))

        cmds.text("\n", height=5)
        cmds.separator()
        cmds.text(" ")

        cmds.text("words about this")

        # section two
        frameLayout1 = cmds.frameLayout(width=self.width, label="Wavy Animation", collapse=True, collapsable=True, marginHeight=10,
                                        marginWidth=5, parent=self.typeCol, ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width-10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Create Rig", command=lambda args: CreateBuild().buildObjects())
        cmds.intSliderGrp("frameNum", label="Animation Length", min=MIN_TIME, max=MAX_TIME, value=(MIN_TIME + MAX_TIME)/10.0)
        cmds.floatSliderGrp('deltaScale', label='Swing Angle', field=True, minValue=0, maxValue=1,
                            value=1, columnWidth=[(1, 125), (2, 25), (3, self.width - 150)], cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=3,
                             columnWidth=[(1, (self.width - 10)/3.0), (2, (self.width - 10)/3.0), (3, (self.width - 10)/3.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.text("Swing Axis:")
        cmds.radioCollection('directionCollection')
        cmds.radioButton('xAxis', label='X-Axis', sl=True)
        cmds.radioButton('yAxis', label='Y-Axis', sl=True)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Animate", command=lambda args: Play().forwards())
        cmds.button(label="Stop", command=lambda args: Play().stop())
        cmds.button(label="Delete", command=lambda args: delete())

        cmds.text("\n", height=5)
        cmds.separator()
        cmds.text(" ")

        cmds.text("words about this")

        #put this at end
        winHeight = 0
        for child in cmds.columnLayout(self.typeCol, q=1, ca=1):
            winHeight += eval('cmds.' + cmds.objectTypeUI(child) + '("' + child + '", q=1, h=1)')
        cmds.window(self.window, e=1, h=winHeight)
        cmds.showWindow(self.window)


def reset():
    cmds.currentTime(0, edit=True)


def frameCollapseChanged(mainLayout):
    cmds.evalDeferred(
        "cmds.window('mainUI', e=1, h=sum([eval('cmds.' + cmds.objectTypeUI(child) + '(\\'' + child + '\\', q=1, h=1)') "
        "for child in cmds.columnLayout('" + mainLayout + "', q=1, ca=1)]))")

