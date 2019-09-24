import maya.cmds as cmds

class CharacterModel:
    def __init__(self):
        self.width = 40
        self.secHeight = 50

    def make(self):
        for x in range(2):
            leg = cmds.polyCube(width=self.width/2.0 - 2, d=self.width/2.0, h=self.secHeight)
            cmds.
