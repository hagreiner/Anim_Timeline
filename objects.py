import maya.cmds as cmds
from constants import DIV, MAX_Y_DIST, WATER, ROCKS, GRASS, L_RED, BIRD
import random


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
        r = 100
        self.pointList = packPoints([])

    def circle(self):
        curve = cmds.curve(p=self.pointList)
        cmds.scale(20, 20, 20, curve, relative=True)
        cmds.move(80, 400, -230, curve, relative=True)
        cmds.rotate(0, 0, -90, curve)
        return curve

    def swoop(self):
        return cmds.curve(p=[
            (200, MAX_Y_DIST, -400),
            (200, MAX_Y_DIST + 100, -200),
            (200,  MAX_Y_DIST + 300, 0),
            (-200,  MAX_Y_DIST + 600, 400),
            (-300,  MAX_Y_DIST + 600, 400),
            (200, MAX_Y_DIST + 300, 0),
            (200, MAX_Y_DIST + 100, -200),
            (250, MAX_Y_DIST, -400),
            (200, MAX_Y_DIST, -400),
            ])


def packPoints(pointList):
    exp = 0.75
    numLoops = 5
    y_dist_mult = 5

    valDict = {}
    randMoveList = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0, -1.1]

    for x in range(5):
        inputVal = (exp + x) ** 2
        valDict[x] = inputVal

    x = 0
    for y in range(numLoops):
        random_move_1 = random.choice(randMoveList)
        random_move_2 = random.choice(randMoveList)
        random_move_3 = random.choice(randMoveList)
        random_move_4 = random.choice(randMoveList)
        random_move_5 = random.choice(randMoveList)
        point_1 = x, 0, 0
        if y == 0:
            first = point_1
        point_2 = x + random_move_1, y_dist_mult * 1, valDict[0]
        point_3 = x, y_dist_mult * 2, valDict[1]
        point_4 = x, y_dist_mult * 3, valDict[2]
        point_5 = x + random_move_2, y_dist_mult * 3, valDict[3] + valDict[1]
        if y == (numLoops/2):
            second = point_5
        point_6 = x, y_dist_mult * 2, valDict[3] + valDict[2]
        point_7 = x, y_dist_mult * 1, valDict[3] + valDict[2] + valDict[1]
        point_8 = x + random_move_3, 0, valDict[3] + valDict[2] + valDict[1] + valDict[0]
        point_9 = x, -y_dist_mult * 1, valDict[3] + valDict[2] + valDict[1]
        pointList.append(point_1)
        pointList.append(point_2)
        pointList.append(point_3)
        pointList.append(point_4)
        pointList.append(point_5)
        pointList.append(point_6)
        pointList.append(point_7)
        pointList.append(point_8)
        pointList.append(point_9)
        if (y + 1) == numLoops:
            point_10 = x, -y_dist_mult * 4, valDict[3] + valDict[2] + valDict[1]
            pointList.append(point_10)

            pointList.append(second)
            pointList.append(first)
            break
        else:
            point_10 = x + random_move_4, -y_dist_mult * 2, valDict[3] + valDict[2]
            point_11 = x, -y_dist_mult * 3, valDict[3] + valDict[1]
            point_12 = x, -y_dist_mult * 3, valDict[2]
            point_13 = x + random_move_5, -y_dist_mult * 2, valDict[1]
            point_14 = x, -y_dist_mult * 1, valDict[0]
            pointList.append(point_10)
            pointList.append(point_11)
            pointList.append(point_12)
            pointList.append(point_13)
            pointList.append(point_14)
        x += 3.2
    return pointList


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


class Bird:
    def make(self):
        bird = cmds.polyCylinder(r=3, h=5, ch=False, sx=6)
        bird = bird[0]
        topFaceB = bird + ".f[7]"
        bottomFaceB = bird + ".f[6]"
        sideFaces = bird + ".f[4:5]"
        cmds.polyExtrudeFacet(topFaceB, offset=1, ltx=0.66, ltz=3)
        cmds.polyExtrudeFacet(topFaceB, offset=-1, ltz=1.2)
        cmds.polyExtrudeFacet(topFaceB, offset=-0.2, ltz=1.2)
        cmds.polyExtrudeFacet(topFaceB, offset=0.2, ltz=1.2)
        cmds.polyExtrudeFacet(topFaceB, offset=0.5, ltz=1.2)
        cmds.polyExtrudeFacet(topFaceB, offset=1.5, ltz=1.2, ltx=0.5)
        cmds.polyExtrudeFacet(topFaceB, offset=0.5, ltz=2.4)
        cmds.polyExtrudeFacet(bottomFaceB, offset=1.0, ltz=2.4, ltx=0.6)
        cmds.polyExtrudeFacet(bottomFaceB, lsx=0.3, ltz=4, ltx=0.6)
        cmds.polyExtrudeFacet(bottomFaceB, lsy=1.2, ltz=4, ltx=0.6)
        cmds.polyExtrudeFacet(sideFaces, lsx=0.1, keepFacesTogether=0)
        cmds.polyExtrudeFacet(sideFaces, ltz=4, keepFacesTogether=0)
        cmds.polyExtrudeFacet(bird + ".f[4]", lsy=0.1, ltz=8, lty=-3, keepFacesTogether=0)
        cmds.polyExtrudeFacet(bird + ".f[5]", lsy=0.1, ltz=8, lty=3, keepFacesTogether=0)
        cmds.rotate(180, 0, 180, bird, relative=True)
        cmds.select(bird)
        cmds.hyperShade(assign=BIRD)

        wing = cmds.duplicate(bird)
        cmds.delete(wing[0] + ".f[0:4]", wing[0] + ".f[6:79]", wing[0] + ".f[84:87]")
        cmds.delete(bird + ".f[4:5]", bird + ".f[76:77]", bird + ".f[79:81]", bird + ".f[83:91]")
        cmds.delete(bird + ".f[74:75]")

        cmds.scale(1.2, 1.2, 1.2, wing, relative=True)
        cmds.move(0, -0.6, -0.3, wing, relative=True)
        x2, y2, z2 = findPos(wing[0] + ".f[4]")
        x3, y3, z3 = findPos(wing[0] + ".f[8]")

        cmds.select(d=True)
        cmds.joint(p=(0, 0, 0))
        cmds.joint(p=(x2, y2, z2))
        cmds.joint('joint1', e=True, zso=True, oj='xyz')
        cmds.joint(p=(x3, y3, z3))
        cmds.joint('joint2', e=True, zso=True, oj='xyz')
        cmds.makeIdentity(bird, a=True)
        cmds.makeIdentity(wing, a=True)
        cmds.skinCluster('joint1', 'joint3', wing, tsb=True)

        cmds.polyMirrorFace(wing, mirrorAxis=2, axis=2)
        cmds.polyCloseBorder(bird)
        returnGroup = cmds.group(bird, wing, relative=True)

        return returnGroup, "joint2"


def randomVTX(object, vlist, moveList):
    for vtx in vlist:
        cmds.move(random.choice(moveList), random.choice(moveList), random.choice(moveList),
                  object + ".f[" + str(vtx) + "]", relative=True)


def findPos(objectFace):
    cmds.select(objectFace)
    X, Y, Z = cmds.polyEvaluate(bc=True)
    x1, x2 = X
    xPos = (x1 + x2)/2.0
    y1, y2 = Y
    yPos = (y1 + y2)/2.0
    cmds.select(clear=True)
    z1, z2 = Z
    zPos = (z1 + z2)/2.0
    cmds.select(clear=True)
    return xPos, yPos, zPos
