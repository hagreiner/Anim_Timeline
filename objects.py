import maya.cmds as cmds
from constants import T_HEIGHT, T_WIDTH, BASE_HEIGHT
import random


class Tree:
    def __init__(self):
        self.sx = 8
        self.treeLoops = 5
        self.randomList = list(range(-20, 20))
        self.trunkMove = list(range(-5, 5))
        self.y_movement = (T_HEIGHT - BASE_HEIGHT) / self.treeLoops

    def assemble(self):
        Meshes().body()
        Lines().body()
        Unique().body()


class Lines(Tree):
    trunkPoints = []
    x = 0
    z = 0

    def body(self):

        for y in range(self.treeLoops):
            random_move_X = random.choice(self.randomList)
            random_move_Z = random.choice(self.randomList)
            point = self.x + random_move_X, self.y_movement*y + BASE_HEIGHT, self.x + random_move_Z
            self.x = random_move_X
            self.z = random_move_Z
            Lines.trunkPoints.append(point)
            for num in range(200):
                self.randomList.append(num - 100)
        extrudeCurve = cmds.curve(p=Lines.trunkPoints)
        cmds.polyExtrudeFacet(
            Meshes.base + '.f[' + str(self.sx + 1) + ']', inputCurve=extrudeCurve, divisions=18, rx=90, ch=False)

    def arms(self):
        pass

    def roots(self):
        pass


class Meshes(Tree):
    base = None

    def body(self):
        base = cmds.polyCylinder(r=T_WIDTH, h=BASE_HEIGHT, subdivisionsAxis=self.sx, ch=False)
        cmds.move(0, BASE_HEIGHT/2.0, 0, base, relative=True)
        Meshes.base = base[0]

    def limbs(self):
        pass


class Unique(Tree):
    def body(self):
        cmds.scale(2, 1, 2, Meshes.base + ".f[" + str(self.sx) + "]")
        for edge in range(self.sx):
            cmds.move(0, 0, random.choice(self.trunkMove), Meshes.base + ".e[" + str(edge) + "]", relative=True)

"""
exp = 0.75
    radR = 1
    heightR = 1
    numLoops = 5
    y_dist_mult = 5

    valDict = {}
    ropePoints = []
    randMoveList = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0, -1.1]

    for x in range(5):
        inputVal = (exp+x)**2
        valDict[x] = inputVal

    x=0
    for y in range(numLoops):
        random_move_1 = random.choice(randMoveList)
        random_move_2 = random.choice(randMoveList)
        random_move_3 = random.choice(randMoveList)
        random_move_4 = random.choice(randMoveList)
        random_move_5 = random.choice(randMoveList)
        point_1 = x, 0, 0
        point_2 = x + random_move_1, y_dist_mult*1, valDict[0]
        point_3 = x, y_dist_mult*2, valDict[1]
        point_4 = x, y_dist_mult*3, valDict[2]
        point_5 = x + random_move_2, y_dist_mult*3, valDict[3] + valDict[1]
        point_6 = x, y_dist_mult*2, valDict[3] + valDict[2]
        point_7 = x, y_dist_mult*1, valDict[3] + valDict[2] + valDict[1]
        point_8 = x + random_move_3, 0, valDict[3] + valDict[2] + valDict[1] + valDict[0]
        point_9 = x, -y_dist_mult*1, valDict[3] + valDict[2] + valDict[1]
        ropePoints.append(point_1)
        ropePoints.append(point_2)
        ropePoints.append(point_3)
        ropePoints.append(point_4)
        ropePoints.append(point_5)
        ropePoints.append(point_6)
        ropePoints.append(point_7)
        ropePoints.append(point_8)
        ropePoints.append(point_9)
        if (y + 1) == numLoops:
            point_10 = x, -y_dist_mult * 4, valDict[3] + valDict[2] + valDict[1]
            ropePoints.append(point_10)
            break
        else:
            point_10 = x + random_move_4, -y_dist_mult * 2, valDict[3] + valDict[2]
            point_11 = x, -y_dist_mult * 3, valDict[3] + valDict[1]
            point_12 = x, -y_dist_mult*3, valDict[2]
            point_13 = x + random_move_5, -y_dist_mult*2, valDict[1]
            point_14 = x, -y_dist_mult*1, valDict[0]
            ropePoints.append(point_10)
            ropePoints.append(point_11)
            ropePoints.append(point_12)
            ropePoints.append(point_13)
            ropePoints.append(point_14)
        x += 3.2

    extrudeCurve = cmds.curve(p=ropePoints)
    rope = cmds.polyCylinder(r=radR, h=heightR, sx=12, ch=False)
    rope = rope[0]
    cmds.move(0, -heightR/2.0, 0, rope)
    cmds.polyExtrudeFacet(rope + '.f[21]', inputCurve=extrudeCurve, divisions=18*y_dist_mult, rx=90, ch=False)
    cmds.delete(extrudeCurve)

    cmds.move(25, 92-4, -12.5, rope, relative=True)
    return rope

"""