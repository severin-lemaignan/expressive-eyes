#!/usr/bin/env python
import imageio
import PIL
from PIL import Image
from pathlib import Path
import pycozmo
from typing import Dict
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

DEFAULT_EYE = {"CENTER_X": 0, "CENTER_Y": 0,
               "SCALE_X": 1.0, "SCALE_Y": 1.0,
               "ANGLE": 0.0,
               "LOWER_INNER_RADIUS_X": 0.5, "LOWER_INNER_RADIUS_Y": 0.5,
               "LOWER_OUTER_RADIUS_X": 0.5, "LOWER_OUTER_RADIUS_Y": 0.5,
               "UPPER_INNER_RADIUS_X": 0.5, "UPPER_INNER_RADIUS_Y": 0.5,
               "UPPER_OUTER_RADIUS_X": 0.5, "UPPER_OUTER_RADIUS_Y": 0.5,
               "UPPER_LID_Y": 0.0, "UPPER_LID_ANGLE": 0.0, "UPPER_LID_BEND": 0.0,
               "LOWER_LID_Y": 0.0, "LOWER_LID_ANGLE": 0.0, "LOWER_LID_BEND": 0.0
               }


class Face:
    """
Function to produce the standard face.

CENTER_X = (0, -50, 50); CENTER_Y = (0, -50, 50)
SCALE_X = (1.0, 1.0, 1.0); SCALE_Y = (1.0, 1.0, 1.0); ANGLE = (0.0, 0.0, 360.0)

LOWER RADIUS:

INNER_X = (0.5, 0.0, 1.0); INNER_Y = (0.5, 0.0, 0.6)

OUTER_X = (0.5, 0.0, 1.0); OUTER_Y = (0.5, 0.0, 5.0)

UPPER RADIUS:

INNER_X = (0.5, 0.0, 1.0); INNER_Y = (0.5, 0.0, 0.6)

OUTER_X = (0.5, 0.0, 1.0); OUTER_Y = (0.5, 0.0, 5.0)

UPPER LID:

Y = (0.0, 0.0, 1.0); ANGLE = (0.0, -60.0, 60.0); BEND = (0.0, 0.0, 1.0)

LOWER LID:

Y = (0.0, 0.0, 1.0); ANGLE = (0.0, -60.0, 60.0); BEND = (0.0, 0.0, 1.0)
    """

    def __init__(self, eye_parameters_left=Dict[str, any], eye_parameters_right=Dict[str, any]):
        master = []; def_items_right = []; def_items_left = []  # Why can't we only hav one def_item?
        for k, v in DEFAULT_EYE.items():
            master.append(k)
            def_items_right.append(v)
            def_items_left.append(v)

        self.left = def_items_left
        self.right = def_items_right

        for s, d in eye_parameters_right.items():
            self.right[master.index(s)] = d

        for j, p in eye_parameters_left.items():
            self.left[master.index(j)] = p

    def render(self):
        face = pycozmo.procedural_face.ProceduralFace(left_eye=self.left, right_eye=self.right)
        return face.render().convert('RGB')

    def interpolateface(self, face, alpha):
        interpolated_left = []
        interpolated_right = []
        for k in range(0, len(self.left)):
            x = [0, 1]
            y = [self.left[k], face.left[k]]
            g = interpolate.interp1d(x, y)
            interpolated_left.append(float(g(alpha)))
        for k in range(0, len(self.right)):
            x = [0, 1]
            y = [self.right[k], face.right[k]]
            h = interpolate.interp1d(x, y)
            interpolated_right.append(float(h(alpha)))

        self.left = interpolated_left
        self.right = interpolated_right
        return self.left, self.right


class AngryFace(Face):
    """
    Function to produce an angry face.

    Standard face is AngryFace(0.6, 30.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_y=0.6, upper_lid_angle=30.0):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle  # Does it matter if the type does agree with this?
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle
            })


class SadFace(Face):
    """
    Function to produce a sad face.

    Standard face is SadFace(0.6, -20.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_y=0.6, upper_lid_angle=-20.0):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle
            })


class HappyFace(Face):
    """
    Function to produce a happy face.

    Standard face is HappyFace(1.0, 1.0, 0.4, 0.4)

    UPPER_INNER_RADIUS_X = (0.5, 0.0, 1.0); UPPER_OUTER_X = (0.5, 0.0, 1.0);
    LOWER LID_Y = (0.0, 0.0, 1.0); LOWER_LID_BEND = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_outer_radius_x=1.0, upper_inner_radius_x=1.0, lower_lid_y=0.4, lower_lid_bend=0.4):
        super().__init__(
            {
                "UPPER_OUTER_RADIUS_X": upper_outer_radius_x,
                "UPPER_INNER_RADIUS_X": upper_inner_radius_x,
                "LOWER_LID_Y": lower_lid_y,
                "LOWER_LID_BEND": lower_lid_bend
            },
            {
                "UPPER_OUTER_RADIUS_X": upper_outer_radius_x,
                "UPPER_INNER_RADIUS_X": upper_inner_radius_x,
                "LOWER_LID_Y": lower_lid_y,
                "LOWER_LID_BEND": lower_lid_bend
            })


def main():
    # face2 = HappyFace()
    # face1 = SadFace()
    # face3 = face2.interpolateface(face1, 0.5)
    # im = face1.render()
    # im1 = face2.render()
    # im2 = Face.render(face3)
    # im1.show()
    # im.show()
    # im2.show()
    # # Annoyed
    # test_face = pycozmo.procedural_face.ProceduralFace(left_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    #                                                              0.5, 0.5, 0.0, -30.0, 0.0, 0.3, -10.0, 0.0],
    #                                                    right_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5,
    #                                                               1.0, 0.5, 0.2, 30.0, 0.0, 0.4, 5.0, 0.0])
    # im1 = test_face.render()
    # im1.show()
# happy_face = HappyFace()
# sad_face = SadFace()
#
# for i in range(20):
#     inbetween = happy_face.interpolate(sad_face, 1./i)
#     im = inbetween.render()
#     im.show()
#
# interpolating_face = happy_face.interpolate(sad_face)
# face = interpolating_face(alpha)
# frames = [face2, face1]
# frames[0].save('out.gif', save_all=True)


if __name__ == '__main__':
    main()
