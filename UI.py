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

        self.typeWin = cmds.window(self.window, title="UV Animation Timeline",
                                   minimizeButton=False, maximizeButton=False, sizeable=False)

    def baseUI(self):
        cmds.columnLayout(self.column, parent=self.typeWin)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.button(label="BUILD SCENE", command=lambda args: CreateBuild().buildObjects())
        cmds.intSliderGrp("frameNum", label="Number of Frames", field=True,
                          minValue=MIN_TIME, maxValue=MAX_TIME, value=MIN_TIME,
                          columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])
        cmds.floatSliderGrp("deltaScale", label="Scale", field=True,
                            minValue=0, maxValue=1, value=0.5, s=0.01,
                            columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.button(label="PLAY", command=lambda args: Play().forwards())
        # cmds.button(label="REVERSE", command=lambda args: Play().backwards())
        cmds.button(label="STOP", command=lambda args: Play().stop())
        cmds.button(label="RESET", command=lambda args: reset())
        cmds.button(label="QUIT", command=lambda args: end())
        cmds.button(label="DEMO", command=lambda args: openMayaStuff.demo())
        cmds.showWindow(self.window)


def reset():
    cmds.currentTime(0, edit=True)
