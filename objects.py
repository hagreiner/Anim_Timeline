import maya.cmds as cmds
from constants import DIV, MAX_Y_DIST, WATER, ROCKS, GRASS, L_RED
import random

# sets -e -forceElement WATERCOLORSG
class Plane:
    def __init__(self):
        self.width = 1000
        self.pointList = []
        self.vtxList = [7, 8, 9, 10, 13, 14, 15, 16, 19, 20, 21, 22, 25, 26, 27, 28]
        self.moveList = list(range(0, 8))
        self.rotate = list(range(-20, 20))
        self.bigMove = list(range(-50, 50))
        self.lightList = []

    def make(self):
        plane = cmds.polyPlane(w=self.width, h=self.width, sx=DIV, sy=DIV)
        cmds.polySoftEdge(plane, a=0)
        cmds.select(plane)
        cmds.hyperShade(assign=WATER)
        return plane[0]


class Curves:
    def __init__(self):
        pass

    def create(self):
        return cmds.curve(p=[(0, 100, 0), (50, 50, 0), (0, 50, 50), (0, 150, 50)])


class StaticObjects(Plane):
    def make(self):
        island = cmds.polyPlane(w=self.width/5, h=self.width/5, sx=5, sy=5)
        island = island[0]
        cmds.move(0, -MAX_Y_DIST, 0, island)
        cmds.move(0, 2 * MAX_Y_DIST, 0, island + ".f[16:18]", island + ".f[11:13]", island + ".f[6:8]", relative=True)
        randomVTX(island, self.vtxList, self.moveList)

        cmds.select(island)
        cmds.hyperShade(assign=ROCKS)
        cmds.select(island + ".f[16:18]", island + ".f[11:13]", island + ".f[6:8]")
        cmds.hyperShade(assign=GRASS)
        cmds.polySoftEdge(island, a=0)

        for x in range(1):
            island_2 = cmds.duplicate(island)
            self.lightList.append(island_2)

        for mesh in self.lightList:
            mesh = mesh[0]
            cmds.select(mesh)
            cmds.hyperShade(assign=ROCKS)
            cmds.select(mesh + ".f[16:18]", mesh + ".f[11:13]", mesh + ".f[6:8]")
            cmds.hyperShade(assign=GRASS)
            randomVTX(mesh, self.vtxList, self.moveList)
            cmds.move(0, -MAX_Y_DIST/2.0 + 20, 0, mesh + ".f[16:18]", mesh + ".f[11:13]", mesh + ".f[6:8]", relative=True)
            cmds.rotate(0, random.choice(self.rotate), 0, mesh, relative=True)
            cmds.move(random.choice(self.bigMove), random.choice(self.moveList) * -1, random.choice(self.bigMove),
                      mesh, relative=True)

        lighthouse = cmds.polyCylinder(r=self.width/22, h=10, sx=8, ch=False)
        cmds.move(0, MAX_Y_DIST, 0, lighthouse)

        lighthouse = lighthouse[0]
        cmds.select(lighthouse)
        cmds.hyperShade(assign=L_RED)
        topFace = lighthouse + ".f[" + str(9) + "]"

        cmds.move(0, 30, 0, topFace, relative=True)
        cmds.polyExtrudeFacet(topFace, offset=6)
        cmds.polyExtrudeFacet(topFace, offset=7, ltz=175)
        cmds.polyExtrudeFacet(topFace, offset=-5)
        cmds.polyExtrudeFacet(topFace, ltz=10)
        cmds.polyExtrudeFacet(topFace, offset=5)
        cmds.polyExtrudeFacet(topFace, ltz=40)
        cmds.polyExtrudeFacet(topFace, offset=-7)
        cmds.polyExtrudeFacet(topFace, offset=30, ltz=20)
        cmds.polyExtrudeFacet(lighthouse + ".f[50:57]", offset=5, keepFacesTogether=0)
        cmds.polyExtrudeFacet(lighthouse + ".f[50:57]", ltz=-2)
        cmds.select(lighthouse + ".f[50:57]")
        cmds.hyperShade(assign=WATER)


def randomVTX(object, vlist, moveList):
    for vtx in vlist:
        cmds.move(random.choice(moveList), random.choice(moveList), random.choice(moveList),
                  object + ".f[" + str(vtx) + "]", relative=True)
