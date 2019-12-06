import maya.cmds as cmds


def createHandle(start, end, name):
    handle = cmds.ikHandle(sj=start, ee=end, pcv=True, p=1, n=name)
    return handle


def createNurbsHandle(nurbsLocationList, nurbsSize, nurbsRotation, ik, addedLocatorList, freeze):
    cmds.spaceLocator(n='ik_loc_' + ik)
    position = cmds.xform(ik, q=True, ws=True, t=True)
    cmds.xform('ik_loc_' + ik, ws=True, t=position)
    cmds.move(addedLocatorList[0], addedLocatorList[1], addedLocatorList[2], "ik_loc_" + ik, relative=True)
    freezeTransformation('ik_loc_' + ik)
    cmds.poleVectorConstraint('ik_loc_' + ik, ik, weight=1)

    circle = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=1, name="circle_" + ik, ch=False)
    circle = circle[0]
    cmds.scale(nurbsSize[0], nurbsSize[1], nurbsSize[2], circle)
    cmds.move(nurbsLocationList[0], nurbsLocationList[1], nurbsLocationList[2], circle, relative=True)
    cmds.rotate(nurbsRotation[0], nurbsRotation[1], nurbsRotation[2], circle, relative=True)

    if freeze == True:
        freezeTransformation(circle)

    cmds.parentConstraint(circle, ik, mo=True)
    cmds.parentConstraint(circle, "ik_loc_" + ik, mo=True)

    return circle


def freezeTransformation(item):
    cmds.makeIdentity(item, apply=True, t=1, r=1, s=1, n=0)
