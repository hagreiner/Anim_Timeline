import maya.cmds as cmds
import maya.mel as mel
from materials import AssignShader


class CreateBuild:
    cube = None
    plane = None

    def buildObjects(self):
        cube = cmds.polyCube(w=50, h=50, d=50, ch=False)
        cmds.move(30 + 50, 25, 0, cube, relative=True)
        CreateBuild.cube = cube[0]
        cmds.polyPlanarProjection(CreateBuild.cube, pc=(0, 0, 0), imageScale=(0.001, 0.001))
        cmds.polyMoveUV(CreateBuild.cube, tu=-0.55, tv=-0.5)
        cmds.select(CreateBuild.cube)
        cmds.delete(ch=True)
        AssignShader(object=CreateBuild.cube).add()
        plane = cmds.polyPlane(w=50, h=50, ch=False)
        cmds.move(-30 - 50, 0, 0, plane, relative=True)
        CreateBuild.plane = plane[0]


class Play:
    def forwards(self):
        Play().stop()
        LoadClipOne(direction="forward", object=CreateBuild.cube).load()
        cmds.play(forward=True)

    def backwards(self):
        Play().stop()
        LoadClipOne(direction="backwards", object=CreateBuild.cube).load()
        cmds.play(forward=True)

    def stop(self):
        cmds.play(state=False)


class LoadClipOne:
    def __init__(self, direction, object):
        if direction == "forward":
            self.direction = 0
        else:
            self.direction = 250
        if object == CreateBuild.cube:
            self.object = "objectCube"
        if object == CreateBuild.plane:
            self.object = "objectPlane"

    def load(self):
        (ClipDictionary().dicts(self.direction)[self.object]).keys()
        # https://download.autodesk.com/us/maya/2009help/CommandsPython/setAttr.html
        # https://lesterbanks.com/2018/04/animate-textures-objects-maya/
        # https: // www.youtube.com / watch?v = UnGvFIQVfZ4


class ClipDictionary:
    def dicts(self, value):
        clips = {
            "objectCube": {
                1: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[0, 10], v=abs(value)),
                2: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[10, 20], v=abs(value - 50)),
                3: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[20, 30], v=abs(value - 100)),
                4: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[30, 40], v=abs(value - 150)),
                5: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[40, 50], v=abs(value - 200)),
                6: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[50, 60], v=abs(value - 250)),
            },
            "objectPlane": {
                1: cmds.setKeyframe(CreateBuild.plane, attribute='translateX', t=[0, 10], v=-abs(value)),
                2: cmds.setKeyframe(CreateBuild.plane, attribute='translateX', t=[10, 20], v=-abs(value - 50)),
                3: cmds.setKeyframe(CreateBuild.plane, attribute='translateX', t=[20, 30], v=-abs(value - 100)),
                4: cmds.setKeyframe(CreateBuild.plane, attribute='translateX', t=[30, 40], v=-abs(value - 150)),
                5: cmds.setKeyframe(CreateBuild.plane, attribute='translateX', t=[40, 50], v=-abs(value - 200)),
                6: cmds.setKeyframe(CreateBuild.plane, attribute='translateX', t=[50, 60], v=-abs(value - 250)),
            }
        }
        return clips


def reset():
    cmds.currentTime(1, edit=True)