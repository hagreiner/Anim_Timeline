import maya.cmds as cmds
from constants import MAX_TIME, MIN_TIME
from timeLine import CreateBuild, Play, LoadCurves
from functools import partial
import edgeLoops
import logPoses


def start():
    """
    :summary: the function that is called to start the UI, sets the timeline to 30fps, and resets the timeline
    :parameter: none
    :return: nothing
    """
    cmds.currentUnit(time='ntsc')
    reset()
    MainMenu().presetUp()


def end():
    """
    :summary: closes the main UI window
    :parameter: none
    :return: nothing
    """
    reset()
    if cmds.window("mainUI", exists=True):
        cmds.deleteUI("mainUI", window=True)


def delete():
    """
    :summary: selects everything in the scene and then deletes it
    :parameter: none
    :return: nothing
    """
    cmds.select(all=True)
    cmds.delete()


def assignValueToPose():
    MainMenu.poseNum = cmds.intField("poseNum", query=True, value=True) - 1


class MainMenu:
    poseNum = 0

    def __init__(self):
        self.col = "mainCol"
        self.window = "mainUI"
        self.width = 300
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.window = cmds.window(self.window, title="Posing Tool",
                                  minimizeButton=False, maximizeButton=False, sizeable=False)

    def presetUp(self):
        self.typeCol = cmds.columnLayout(self.col, parent=self.window)
        cmds.rowColumnLayout(numberOfColumns=1, parent=self.typeCol)
        cmds.text("Select Rig", h=40, width=self.width)
        cmds.button(label="Confirm", command=lambda args: (assignValueToPose(), MainMenu().start(), LoadCurves().add()),
                    height=25, width=50)  # needs to also log them
        cmds.text("Number of Poses", h=40)
        cmds.intField("poseNum", min=1, max=50, value=4, width=50)

        cmds.showWindow(self.window)

    def start(self):
        """
        :summary: is called in the start() function, contains the main UI for the scripts
        :parameter: none
        :return: nothing
        """
        self.typeCol = cmds.columnLayout(self.col, parent=self.window, w=self.width)

        # section one - this was removed

        # section two
        frameLayout1 = cmds.frameLayout(width=self.width, label="Log Poses", collapse=True, collapsable=True, marginHeight=10,
                                        marginWidth=5, parent=self.typeCol, ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, (self.width - 10)/2.0), (2, (self.width - 10)/2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.button(label="Pose " + str(0),
                    command=lambda args: logPoses.findPoseInformation().savePose("Pose_" + str(0)), height=20)
        cmds.textField("Pose_" + str(0), en=False, text="None", height=20)

        for number in range(MainMenu.poseNum):
            cmds.button(label="Pose " + str(number + 1),
                        command=lambda args: logPoses.findPoseInformation().savePose("Pose_" + str(number + 1)),
                        height=20)
            cmds.textField("Pose_" + str(number + 1), en=False, text="None", height=20)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Confirm All Poses", command=lambda args: None)

        cmds.text("", h=5)

        poseChildren = cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 10) / 2.0), (2, (self.width - 20) / 2.0)],
                             parent=frameLayout1, co=[1, "both", 5])
        cmds.text("Pose " + str(0))
        cmds.intSlider("Pose_Length_" + str(0), min=0, max=5, value=0)

        for number in range(MainMenu.poseNum):
            cmds.text("Pose " + str(number+1))
            cmds.intSlider("Pose_Length_" + str(number+1), min=0, max=5, value=0)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.button(label="Animate Cycle", command=lambda args: Play().forwardsRig())
        cmds.button(label="Stop", command=lambda args: Play().stop())
        cmds.button(label="Reset", command=lambda args: logPoses.Reset().resetPosesAndUI())

        cmds.text("\n", height=5)
        cmds.separator()
        cmds.text(" ")

        cmds.button(label="About this Tool", command=lambda args: InfoWindow(type="userPoses").create())

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

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.separator()
        cmds.button(label="Quit", command=lambda args: end())

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

        if type == "userPoses":
            self.informationList = userPoseHelp()

    def create(self):
        """
        :summary: a help window that is called from the MainMenu class
        :parameter: type determines the function that will be called for the text in this window
        :return: nothing
        """
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
    """
    :summary: resets the current time on the timeline to zero
    :parameter: none
    :return: nothing
    """
    cmds.currentTime(0, edit=True)


def frameCollapseChanged(mainLayout):
    """
    :summary: updates the height of the column frames within it are collapsed or expanded
    :param mainLayout: the column
    :return: nothing
    """
    cmds.evalDeferred(
        "cmds.window('mainUI', e=1, h=sum([eval('cmds.' + cmds.objectTypeUI(child) + '(\\'' + child + '\\', q=1, h=1)') "
        "for child in cmds.columnLayout('" + mainLayout + "', q=1, ca=1)]))")


def rigHelp():
    """
    :summary: returns information about rig creation that will appear in the help window
    :parameter: none
    :return: a list of lines of text
    """
    return [
        " - select faces, vertices, or edges the correspond with the joint type",
        " - press the button for the joint to assign it to a position",
        " - pressing the first button will place the joints in world space",
        " - pressing the second button will connect the joints and create basic ik with handles",
        " - included ik handles are: arm movement, arm rotation, leg movement, and foot controls",
    ]


def userPoseHelp():
    """
    :summary: returns information about user pose creation that will appear in the help window
    :parameter: none
    :return: a list of lines of text
    """
    return [
        " - move the nurbs handles",
        " - press the button to confirm the pose",
        " - confirm all poses to load them and then animate them",
        " - the pose sliders will determine the length of the pose",
    ]
