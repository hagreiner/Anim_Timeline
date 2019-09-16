import maya.cmds as cmds
from constants import WATER, ROCKS, GRASS, L_RED, BIRD


class AssignColor:
    def __init__(self):
        pass

    def water(self):
        shd = cmds.shadingNode('lambert', name=WATER, asShader=True)
        cmds.setAttr(shd + ".color", 0.24219, 0.972818, 1.242, type='double3')
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        cmds.sets(WATER, e=True, forceElement=shdSG)

    def rocks(self):
        shd = cmds.shadingNode('lambert', name=ROCKS, asShader=True)
        cmds.setAttr(shd + ".color",  0.629, 0.483821, 0.406963, type='double3')
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        cmds.sets(ROCKS, e=True, forceElement=shdSG)

    def grass(self):
        shd = cmds.shadingNode('lambert', name=GRASS, asShader=True)
        cmds.setAttr(shd + ".color", 0.629, 0.8, 0.406963, type='double3')
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        cmds.sets(GRASS, e=True, forceElement=shdSG)

    def lred(self):
        shd = cmds.shadingNode('lambert', name=L_RED, asShader=True)
        cmds.setAttr(shd + ".color", 0.929, 0.4, 0.406963, type='double3')
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        cmds.sets(L_RED, e=True, forceElement=shdSG)

    def bird(self):
        shd = cmds.shadingNode('lambert', name=BIRD, asShader=True)
        cmds.setAttr(shd + ".color", 0.84, 0.84, 1.0, type='double3')
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        cmds.sets(BIRD, e=True, forceElement=shdSG)