import maya.cmds as cmds
from constants import DIV


class Plane:
    def __init__(self):
        self.width = 1000
        self.height = 10
        self.pointList = []

    def make(self):
        plane = cmds.polyPlane(w=self.width, h=self.width, sx=DIV, sy=DIV)
        return plane[0]
