import maya.cmds as cmds
from constants import WIDTH, MAX_TIME, MIN_TIME, MAX_Y_DIST, MIN_Y_DIST
from timeLine import CreateBuild, Play


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
        cmds.intSliderGrp("numWaves", label="Number of Waves", field=True,
                          minValue=1, maxValue=10, value=1,
                          columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])
        cmds.intSliderGrp("distanceYMax", label="Y Max", field=True,
                          minValue=MIN_Y_DIST, maxValue=MAX_Y_DIST, value=MIN_Y_DIST,
                          columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])
        cmds.intSliderGrp("distanceYMin", label="Y Min", field=True,
                          minValue=MIN_Y_DIST, maxValue=MAX_Y_DIST, value=MIN_Y_DIST,
                          columnWidth=[(1, 100), (2, 50), (3, WIDTH-125)],  cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)
        cmds.button(label="PLAY", command=lambda args: Play().forwards())
        # cmds.button(label="REVERSE", command=lambda args: Play().backwards())
        cmds.button(label="STOP", command=lambda args: Play().stop())
        cmds.button(label="RESET", command=lambda args: reset())
        cmds.button(label="QUIT", command=lambda args: end())
        cmds.showWindow(self.window)


def reset():
    cmds.currentTime(0, edit=True)
