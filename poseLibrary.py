import maya.cmds as cmds


def nurbsList():
    return [
        "circle_Right_Foot",
        "circle_Right_Leg",
        "circle_Left_Foot",
        "circle_Left_Leg",
        "circle_Right_Arm",
        "circle_Right_Arm_Rot",
        "circle_Left_Arm",
        "circle_Left_Arm_Rot",
        "circle_Center_Bend",
    ]


def default():
    # legs, arms, core
    return ({
        "legs": {
            0: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 0.0, 0.0],
                'circle_Left_Leg': [0.0, 0.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
            1: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 18.0, 24.0],
                'circle_Left_Leg': [0.0, 0.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
            2: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 2.0, -5.5],
                'circle_Left_Leg': [0.0, 0.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
            3: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 0.0, 0.0],
                'circle_Left_Leg': [0.0, 0.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
    },
        "arms": {
            0: {'circle_Right_Arm': [0.0, 0.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [0.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [0.0, 0.0, 0.0],
                },
            1: {'circle_Right_Arm': [32.0, 38.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [5.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [-10.0, 0.0, 0.0],
                },
            2: {'circle_Right_Arm': [32.0, 38.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [10.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [-20.0, 0.0, 0.0],
                },
            3: {'circle_Right_Arm': [0.0, 0.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [0.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [0.0, 0.0, 0.0],
                },
        },
        "core": {
            0: {
                'circle_Center_Bend': [0.0, 0.0, 0.0],
            },
            1: {
                'circle_Center_Bend': [0.0, 0.0, 0.0],
            },
            2: {
                'circle_Center_Bend': [0.0, 0.0, 0.0],
            },
            3: {
                'circle_Center_Bend': [0.0, 0.0, 0.0],
            },
        }
    },
    {
        "legs": {
            0: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 0.0, 0.0],
                'circle_Left_Leg': [0.0, 0.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
            1: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 0, 0.0],
                'circle_Left_Leg': [0.0, 5.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
            2: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 0.0, 0.0],
                'circle_Left_Leg': [0.0, -40.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
            3: {'circle_Right_Foot': [0.0, 0.0, 0.0], 'circle_Right_Leg': [0.0, 0.0, 0.0],
                'circle_Left_Leg': [0.0, 0.0, 0.0], 'circle_Left_Foot': [0.0, 0.0, 0.0]
                },
    },
        "arms": {
            0: {'circle_Right_Arm': [0.0, 0.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [0.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [0.0, 0.0, 0.0],
                },
            1: {'circle_Right_Arm': [0.0, 0.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [0.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [0.0, 0.0, 0.0],
                },
            2: {'circle_Right_Arm': [0.0, 0.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [0.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [0.0, 0.0, 0.0],
                },
            3: {'circle_Right_Arm': [0.0, 0.0, 0.0], 'circle_Left_Arm_Rot': [0.0, 0.0, 0.0],
                'circle_Left_Arm': [0.0, 0.0, 0.0],  'circle_Right_Arm_Rot': [0.0, 0.0, 0.0],
                },
        },
        "core": {
            0: {
                'circle_Center_Bend': [0.0, 0.0, 0.0],
            },
            1: {
                'circle_Center_Bend': [0.0, -15.0, 0.0],
            },
            2: {
                'circle_Center_Bend': [0.0, -30.0, 0.0],
            },
            3: {
                'circle_Center_Bend': [0.0, 0.0, 0.0],
            },
        }
    })

