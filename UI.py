import maya.cmds as cmds
from constants import WIDTH, SHADER_NAME
from timeLine import CreateBuild, Play
from materials import CreateShader


def start():
    if cmds.window("build", exists=True):
        cmds.deleteUI("build", window=True)

    if cmds.window("props", exists=True):
        cmds.deleteUI("props", window=True)

    if cmds.objExists(SHADER_NAME) == False:
        CreateShader().create()

    cmds.currentUnit(time='ntsc')
    reset()

    MainUI().baseUI()


def end():
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
        cmds.button(label="PLAY", command=lambda args: Play().forwards())
        cmds.button(label="REVERSE", command=lambda args: Play().backwards())
        cmds.button(label="STOP", command=lambda args: Play().stop())
        cmds.button(label="RESET", command=lambda args: reset())
        cmds.button(label="QUIT", command=lambda args: end())
        cmds.showWindow(self.window)


def reset():
    cmds.currentTime(1, edit=True)