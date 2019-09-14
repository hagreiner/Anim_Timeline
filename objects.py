import maya.cmds as cmds
from constants import DIV, MAX_Y_DIST
import random


class Plane:
    def __init__(self):
        self.width = 1000
        self.pointList = []
        self.vtxList = [7, 8, 9, 10, 13, 14, 15, 16, 19, 20, 21, 22, 25, 26, 27, 28]
        self.moveList = list(range(0, 8))

    def make(self):
        plane = cmds.polyPlane(w=self.width, h=self.width, sx=DIV, sy=DIV)
        return plane[0]


class Curves:
    def __init__(self):
        pass

    def create(self):
        pass


class StaticObjects(Plane):
    def make(self):
        island = cmds.polyPlane(w=self.width/5, h=self.width/5, sx=5, sy=5)
        island = island[0]
        cmds.move(0, -MAX_Y_DIST, 0, island)
        cmds.move(0, 2* MAX_Y_DIST, 0, island + ".f[16:18]", island + ".f[11:13]", island + ".f[6:8]", relative=True)
        for vtx in self.vtxList:
            cmds.move(random.choice(self.moveList), random.choice(self.moveList), random.choice(self.moveList),
                      island + ".f[" + str(vtx) + "]", relative=True)
