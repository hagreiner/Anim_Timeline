import maya.cmds as cmds
from constants import DIV_NUM, DIV


class Plane:
    def __init__(self):
        self.width = 1000
        self.height = 10
        self.pointList = []

    def make(self):
        plane = cmds.polyCube(w=20, h=self.height, d=self.width, ch=False)
        for x in range(DIV_NUM/2):
            point = 20*x + 5, 0, 0
            self.pointList.append(point)
        extrudeCurve = cmds.curve(p=self.pointList)
        cmds.polyExtrudeFacet(plane[0] + '.f[4]', inputCurve=extrudeCurve, divisions=DIV_NUM)
        cmds.delete(plane[0] + ".f[0]", plane[0] + ".f[2:205]", plane[0] + ".f[306:405]")

        plane2 = cmds.polyPlane(w=self.width, h=self.width, sx=DIV, sy=DIV)
        cmds.move(500, 0, -1100, plane2)

        return extrudeCurve, plane2[0]