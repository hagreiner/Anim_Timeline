import maya.cmds as cmds


def createHandle(start, end, name):
    """
    :summary: creates an ik handle
    :param start: the starting joint
    :param end: the ik end effector
    :param name: name of the handle
    :return: the ik handle
    """
    handle = cmds.ikHandle(sj=start, ee=end, pcv=True, p=1, n=name)
    return handle


def createNurbsHandle(nurbsLocationList, nurbsSize, nurbsRotation, ik, addedLocatorList, freeze):
    """
    :summary: adds pole vectors, locators, and nurbs handles to an ik handle
    :param nurbsLocationList: when the nurbs handle should be
    :param nurbsSize: the size of the nurbs handle
    :param nurbsRotation: the rotation of the nurbs handle
    :param ik: the name of the ik handle
    :param addedLocatorList: an extra movement that should be added to the locator
    :param freeze: a boolean that says if transforms should be frozen or not
    :return: the nurbs handle
    """
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
    """
    :summary: sets the transforms, rotations, and scale to 1 or 0
    :param item: the object that is being reset
    :return: none
    """
    cmds.makeIdentity(item, apply=True, t=1, r=1, s=1, n=0)
