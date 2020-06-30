#!/usr/bin/env python
import imageio
import PIL
from PIL import Image
from pathlib import Path
import pycozmo
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

    def __init__(self, eye_parameters_left, eye_parameters_right):
        master = []; def_items = []
        for k, v in DEFAULT_EYE.items():
            master.append(k)
            def_items.append(v)

        left_eye = def_items
        right_eye = def_items

        for s, d in eye_parameters_right.items():
            right_eye[master.index(s)] = d

        self.right = right_eye

        for j, p in eye_parameters_left.items():
            left_eye[master.index(j)] = p

        self.left = left_eye

    def render(self):
        face = pycozmo.procedural_face.ProceduralFace(left_eye=self.left, right_eye=self.right)
        return face.render().convert('RGB')


class interpolate(Face):
    def __init__(self, upper_lid_y, upper_lid_angle):
        input_left = face()
        input_right = face()
        interpolated_left = self.left
        interpolated_right = self.right
        for k in self.left:
            x = [0, alpha]
            y = [self.left[k], face[k]]
            f = interpolate.interp1d(x, y)
            interpolated_left[k] = f(y)
        for k in self.right:
            x = [0, alpha]
            y = [self.right[k], face[k]]
            f = interpolate.interp1d(x, y)
            interpolated_right[k] = f(y)
        super().__init__(interpolated_left, interpolated_right)

        # return interpolated_face


class AngryFace(Face):
    """
    Function to produce an angry face.

    Standard face is AngryFace(0.5, 30.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """

    def __init__(self, upper_lid_y, upper_lid_angle):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle  # Need to make this negative value work
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

    def __init__(self, upper_lid_y, upper_lid_angle):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle  # Need to make this negative value work
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle
            })


face2 = AngryFace(0.5, 30.0)


def main():
    im1 = face2.render()
    im1.show()


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
