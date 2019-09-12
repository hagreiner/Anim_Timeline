import maya.cmds as cmds
from constants import T_HEIGHT, T_WIDTH, BASE_HEIGHT
import random


# def clear():
#     Lines.bodyCurve = None
#     Lines.trunkPoints = []
#     Lines.x = 0
#     Lines.y = 0
#     Meshes.base = None


class Tree:
    def __init__(self):
        self.sx = 8
        self.treeLoops = 5
        self.smallMove = (list(range(-100, 100)))
        self.trunkMove = list(range(-5, 5))
        self.y_movement = (T_HEIGHT - BASE_HEIGHT) / self.treeLoops
        self.armLength = list(range(20, 50))
        self.armWidth = list(range(5, 10))
        self.moveArm = findPosition()

    def assemble(self):
        Meshes().body()
        Lines().body()
        Unique().body()
        CreateArms().make()
        return Lines.bodyCurve


class Lines(Tree):
    bodyCurve = None
    armCurve1 = None
    armCurve2 = None
    trunkPoints = []
    arm1Points = []
    arm2Points = []

    def body(self):
        point_1 = 0, BASE_HEIGHT, 0
        Lines.trunkPoints.append(point_1)
        point_2 = 20, self.y_movement*1, 0
        Lines.trunkPoints.append(point_2)
        point_3 = 0, self.y_movement*2, 20
        Lines.trunkPoints.append(point_3)
        point_4 = 20, self.y_movement*3, 0
        Lines.trunkPoints.append(point_4)
        point_5 = 0, self.y_movement*4, 20
        Lines.trunkPoints.append(point_5)
        Lines.bodyCurve = cmds.curve(p=Lines.trunkPoints)
        cmds.polyExtrudeFacet(
            Meshes.base + '.f[' + str(self.sx + 1) + ']', ls=(0.2, 0.2, 0.2), inputCurve=Lines.bodyCurve, divisions=15,
            rx=90, ch=False)

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


class Unique(Tree):
    def body(self):
        cmds.scale(2, 1, 2, Meshes.base + ".f[" + str(self.sx) + "]")
        for edge in range(self.sx):
            cmds.move(0, 0, random.choice(self.trunkMove), Meshes.base + ".e[" + str(edge) + "]", relative=True)
        cmds.select(Meshes.base)
        loopNum = cmds.polyEvaluate(v=True)
        cmds.select(clear=True)
        for vtx in range(loopNum):
            cmds.move(random.choice(self.smallMove)/100.0, random.choice(self.smallMove)/100.0,
                      random.choice(self.smallMove)/100.0, Meshes.base + ".vtx[" + str(vtx) + "]", relative=True)


class CreateArms(Tree):
    def make(self):
        for x in range(5):
            arm = cmds.polyCylinder(r=random.choice(self.armWidth), h=1, ch=False, name="arm_#")
            cmds.rotate(0, 0, 90, arm)
            cmds.move(0, random.choice(self.moveArm), 0, arm)
            Lines().arms()


def findPosition():
    cmds.select(Meshes.base)
    X, Y, Z = cmds.polyEvaluate(v=True)
    cmds.select(clear=True)


    """
    [18] ;
select -tgl pCylinder1.f[36] ;
select -tgl pCylinder1.f[44] ;
select -tgl pCylinder1.f[103] ;
select -tgl pCylinder1.f[97] 
    :return: 
    """
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