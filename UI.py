import maya.cmds as cmds
from constants import WIDTH, MAX_TIME, MIN_TIME, MAX_X_DIST, MIN_X_DIST
from timeLine import CreateBuild, Play
import openMayaStuff


def start():
    if cmds.window("build", exists=True):
        cmds.deleteUI("build", window=True)

    if cmds.window("props", exists=True):
        cmds.deleteUI("props", window=True)

    cmds.currentUnit(time='ntsc')
    reset()

    MainUI().baseUI()


def end():
    reset()
    cmds.select(all=True)
    cmds.delete()
    if cmds.window("window", exists=True):
        cmds.deleteUI("window", window=True)


class MainUI:
    def __init__(self):
        self.width = WIDTH
        self.window = "window"
        self.column = "col"

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.typeWin = cmds.window(self.window, title="Animation Timeline",
                                   minimizeButton=False, maximizeButton=False, sizeable=False)

    def baseUI(self):
        cmds.columnLayout(self.column, parent=self.typeWin)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.text("STEP ONE", align="center", bgc=[0.5, 0.5, 0.5], h=30)
        cmds.separator()

        cmds.button(label="Build Skeleton", command=lambda args: CreateBuild().buildObjects())

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.separator()
        cmds.text("STEP TWO: Animation Speed", align="center", bgc=[0.5, 0.5, 0.5], h=30)
        cmds.separator()
        cmds.intSliderGrp("frameNum", label="Number of Frames", field=True,
                          minValue=MIN_TIME, maxValue=MAX_TIME, value=MIN_TIME,
                          columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.separator()
        cmds.text("STEP THREE: Animation Scale", align="center", bgc=[0.5, 0.5, 0.5], h=30)
        cmds.separator()
        cmds.floatSliderGrp("deltaScale", label="Scale (current)", field=True,
                            minValue=0, maxValue=1, value=0.5, s=0.01,
                            columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.width/4.0), (2, self.width/4.0 * 3)], parent=self.column)
        cmds.text("Legs Scale", h=20)
        cmds.floatSlider("legScale", minValue=1.0, maxValue=1.05, value=1.0, s=0.01)
        cmds.text("Arms Scale", h=20)
        cmds.floatSlider("armScale", minValue=0.5, maxValue=1, value=0.5, s=0.01)
        cmds.text("Tilt Scale", h=20)
        cmds.floatSlider("tiltScale", minValue=-0.3, maxValue=0.5, value=-0.3, s=0.01)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.separator()
        cmds.text("STEP FOUR: Skeleton Size", align="center", bgc=[0.5, 0.5, 0.5], h=30)
        cmds.separator()

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.separator()
        cmds.text("STEP Five: Start", align="center", bgc=[0.5, 0.5, 0.5], h=30)
        cmds.separator()
        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.button(label="play", command=lambda args: Play().forwards())
        cmds.text("", h=2)
        # cmds.button(label="REVERSE", command=lambda args: Play().backwards())
        cmds.button(label="stop", command=lambda args: Play().stop())
        cmds.text(" ", h=2)
        cmds.button(label="reset", command=lambda args: reset())
        cmds.text("  ", h=2)
        cmds.button(label="quit", command=lambda args: end())
        # cmds.button(label="DEMO", command=lambda args: openMayaStuff.demo())
        cmds.showWindow(self.window)


def reset():
    cmds.currentTime(0, edit=True)
