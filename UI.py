import maya.cmds as cmds
from constants import WIDTH


def start():
    if cmds.window("build", exists=True):
        cmds.deleteUI("build", window=True)

    if cmds.window("props", exists=True):
        cmds.deleteUI("props", window=True)
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
        cmds.button(label="QUIT", command=lambda args: end())
        cmds.showWindow(self.window)
