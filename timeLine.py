import maya.cmds as cmds
import maya.mel as mel


class CreateBuild:
    cube = None
    plane = None

    def buildObjects(self):
        cube = cmds.polyCube(w=50, h=50, d=50, ch=False)
        cmds.move(30 + 50, 25, 0, cube, relative=True)
        CreateBuild.cube = cube[0]
        cmds.polyPlanarProjection(CreateBuild.cube, pc=(0, 0, 0), imageScale=(0.001, 0.001))
        cmds.polyMoveUV(CreateBuild.cube, tu=-0.55, tv=-0.5)
        print(CreateBuild.cube)
        plane = cmds.polyPlane(w=50, h=50, ch=False)
        cmds.move(-30 - 50, 0, 0, plane, relative=True)
        CreateBuild.plane = plane[0]


class Play:
    def forwards(self):
        LoadClipOne(direction="forward").load()
        cmds.play(forward=True)

    def backwards(self):
        LoadClipOne(direction="backwards").load()
        cmds.play(forward=True)

    def stop(self):
        cmds.play(state=False)


class LoadClipOne:
    def __init__(self, direction):
        self.direction = direction

    def load(self):
        pass
        # https://download.autodesk.com/us/maya/2009help/CommandsPython/setAttr.html
        # cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[0, 7], v=0)
        # cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[80, 100], v=80)
        # c = cmds.setAttr(CreateBuild.cube, type="polyFace.mu")
        # cmds.setKeyframe((CreateBuild.cube), hierarchy="none", at="uvpivot", controlPoints=True, shape=True, bd=True, t=[0, 30])
        # # setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 {"pPlane1.f[0:99]"};
        #
        # cmds.polyMoveUV(CreateBuild.cube, tu=1, tv=-0.5)
        # cmds.setKeyframe(CreateBuild.cube + ".uvPivot", bd=True, at="uvPivot", t=[40, 50])