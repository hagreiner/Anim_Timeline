import maya.cmds as cmds
from constants import MAX_TIME
from objects import Tree


class CreateBuild:
    cube = None

    def buildObjects(self):
        # cube = cmds.polyCube(w=50, h=50, d=50, ch=False, name="cube_#")
        # cmds.move(30 + 50, 25, 0, cube, relative=True)
        # CreateBuild.cube = cube[0]
        # plane = cmds.polyPlane(w=50, h=50, ch=False, name="plane_#")
        # cmds.move(-30 - 50, 0, 0, plane, relative=True)
        # CreateBuild.plane = plane[0]
        CreateBuild.cube = Tree().assemble()


class Play:
    frameNum = 10
    distX = 0

    def __init__(self):
        Play.frameNum = cmds.intSliderGrp("frameNum", query=True, value=True)
        Play.distX = cmds.intSliderGrp("distanceX", query=True, value=True)
        cmds.playbackOptions( minTime='0sec', maxTime=str(Play.frameNum/30.0) + 'sec')
        try:
            delFrames(CreateBuild.cube)
        except:
            pass

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
            self.direction = Play.distX
        if object == CreateBuild.cube:
            self.object = "objectCube"

    def load(self):
        (ClipDictionary().dicts(self.direction)[self.object]).keys()


class ClipDictionary:
    def dicts(self, value):
        clips = {
            "objectCube": {
                1: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[calcFrames()[0], calcFrames()[1]], v=abs(value)),
                2: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[calcFrames()[1], calcFrames()[2]], v=abs(value - (Play.distX / 5.0))),
                3: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[calcFrames()[2], calcFrames()[3]], v=abs(value - 2*(Play.distX / 5.0))),
                4: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[calcFrames()[3], calcFrames()[4]], v=abs(value - 3*(Play.distX / 5.0))),
                5: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[calcFrames()[4], calcFrames()[5]], v=abs(value - 4*(Play.distX / 5.0))),
                6: cmds.setKeyframe(CreateBuild.cube, attribute='translateX', t=[calcFrames()[5], calcFrames()[6]], v=abs(value - 5*(Play.distX / 5.0))),
            }
        }
        return clips


def reset():
    cmds.currentTime(0, edit=True)


def calcFrames():
    return [
        0, Play.frameNum/6, (Play.frameNum/6)*2, (Play.frameNum/6)*3, (Play.frameNum/6)*4, (Play.frameNum/6)*5, (Play.frameNum/6)*6
    ]


def delFrames(object):
    cmds.cutKey(object, time=(0, MAX_TIME), attribute='translateX', option="keys")
