import maya.cmds as cmds
import maya.api.OpenMaya as om
import time
import math

def demo():
    transform_node, shape_node = cmds.polyCube(w=20, h=20, d=20)
    cmds.setAttr(transform_node+".rotateY", 60)
    cmds.setAttr(transform_node+".rotateX", 45)
    cmds.setAttr(transform_node+".rotateZ", 95)

    sel_list = om.MSelectionList()
    sel_list.add(transform_node)
    obj = sel_list.getDependNode(0)


    xform = om.MFnTransform(obj)
    quat = xform.rotation(asQuaternion=True)
    quat.normalizeIt()
    py_quat = [quat[x] for x in range(4)]
    xform.setRotation(om.MQuaternion.kIdentity, om.MSpace.kObject )

    xform.setRotation(quat, om.MSpace.kObject)
    xform.setRotationComponents(py_quat, om.MSpace.kObject, asQuaternion=True)

    q = om.MQuaternion( math.radians(10), om.MVector(0,1,0) )
    xform.rotateBy(q, om.MSpace.kTransform)

    half = om.MQuaternion.slerp(om.MQuaternion.kIdentity, quat, 0.5)
    xform.setRotation(half, om.MSpace.kObject)

    xform.setRotation(om.MQuaternion.kIdentity, om.MSpace.kObject )
    step = om.MQuaternion.slerp(om.MQuaternion.kIdentity, quat, 0.1)
    for x in range(10):
        xform.rotateBy(step, om.MSpace.kObject)
        cmds.refresh()
        time.sleep(0.1)

    joint = cmds.joint(p=(1, 1, 1))
    print cmds.xform(joint, bb=True, query=True)
    print cmds.xform(joint, bbi=True, query=True)
    joint = cmds.polyCube()
    print cmds.xform(joint[0] + ".f[2]", bb=True, query=True)
