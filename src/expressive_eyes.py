#!/usr/bin/env python
import imageio
import PIL
from PIL import Image
from pathlib import Path
import pycozmo
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tkinter
import time

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

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

    def __init__(self, eye_parameters_left={}, eye_parameters_right={}):

        master = list(DEFAULT_EYE.keys())

        self.left = list(DEFAULT_EYE.values())
        self.right = list(DEFAULT_EYE.values())

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

        result = Face()
        result.left = interpolated_left
        result.right = interpolated_right
        return result


class NeutralFace(Face):
    """
    Function to produce the neutral face.

    Standard face is NeutralFace()
    """
    def __init__(self):
        super().__init__(
            {
            },
            {
            })


#  Six basic expressions by Ekman
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
                "UPPER_LID_ANGLE": -upper_lid_angle
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle
            })


class SadFace(Face):
    """
    Function to produce a sad face.

    Standard face is SadFace(0.6, 20.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_y=0.6, upper_lid_angle=20.0):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle
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


class SurprisedFace(Face):
    """
    Function to produce a surprised face.

    Standard face is SurprisedFace(none)

    Surprised face is equal to the default face. The speed of movement to this face should be higher.
    """
    def __init__(self):
        super().__init__()


class DisgustFace(Face):
    """
    Function to produce a disgusted face.

    Standard face is DisgustFace(left_eye=(3.0, 10.0, 0.3), right_eye=(0.2, 20.0, 0.2, 10.0))

    LEFT EYE PARAMETERS:
    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);

    RIGHT EYE PARAMETERS:
    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0)
    """
    def __init__(self, left_eye=(0.3, -10.0, 0.3), right_eye=(0.2, 20.0, 0.2, -10.0)):
        super().__init__(
            {
             "UPPER_LID_Y": left_eye[0],
             "UPPER_LID_ANGLE": -left_eye[1],
             "LOWER_LID_Y": left_eye[2]
            },
            {
             "UPPER_LID_Y": right_eye[0],
             "UPPER_LID_ANGLE": right_eye[1],
             "LOWER_LID_Y": right_eye[2],
             "LOWER_LID_ANGLE": -right_eye[3]
            })


class FearFace(Face):
    """
    Function to produce a fearful face.

    Standard face is FearFace(30.0, 0.1, 0.4, 10.0)

    UPPER_LID_ANGLE = (0.0, -60.0, 60.0); UPPER_LID_BEND = (0.0, 0.0, 1.0)
    LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0)
    """
    def __init__(self, upper_lid_angle=30.0, upper_lid_bend=0.1, lower_lid_y=0.4, lower_lid_angle=10.0):
        super().__init__(
            {
             "UPPER_LID_ANGLE": upper_lid_angle,
             "UPPER_LID_BEND": upper_lid_bend,
             "LOWER_LID_Y": lower_lid_y,
             "LOWER_LID_ANGLE": lower_lid_angle
            },
            {
             "UPPER_LID_ANGLE": -upper_lid_angle,
             "UPPER_LID_BEND": upper_lid_bend,
             "LOWER_LID_Y": lower_lid_y,
             "LOWER_LID_ANGLE": -lower_lid_angle
            })


# Sub-faces of sadness
# Pleading is directional related (i.e. looking up, head down, is normally associated with pleading)
class PleadingFace(Face):
    """
    Function to produce a pleading face.

    Standard face is PleadingFace(20.0, 0.5)

    UPPER_LID_ANGLE = (0.0, -60.0, 60.0); LOWER_LID_Y = (0.0, 0.0, 1.0)
    """
    def __init__(self, upper_lid_angle=30.0, lower_lid_y=0.5):
        super().__init__(
            {
             "UPPER_LID_ANGLE": upper_lid_angle,
             "LOWER_LID_Y": lower_lid_y,
            },
            {
             "UPPER_LID_ANGLE": -upper_lid_angle,
             "LOWER_LID_Y": lower_lid_y,
            })


class VulnerableFace(Face):
    """
    Function to produce a vulnerable face.

    Standard face is VulnerableFace(0.3, 20.0, 0.5, 10.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_y=0.3, upper_lid_angle=20.0, lower_lid_y=0.5, lower_lid_angle=10.0):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
                "LOWER_LID_ANGLE": lower_lid_angle
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
                "LOWER_LID_ANGLE": -lower_lid_angle
            })



class DespairFace(Face):
    """
    Function to produce a despairing face.

    Standard face is DespairFace(0.6, 30.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_y=0.6, upper_lid_angle=30.0):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle
            })


class GuiltyFace(Face):
    """
    Function to produce a guilty face.

    Standard face is GuiltyFace(35, 0.6, 10.0, 0.3)

    CENTER_Y = (0, -50, 50);
    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    UPPER_LID_BEND = (0.0, 0.0, 1.0);
    """
    def __init__(self, center_y=35, upper_lid_y=0.6, upper_lid_angle=10.0, upper_lid_bend=0.3):
        super().__init__(
            {
             "CENTER_Y": center_y,
             "UPPER_LID_Y": upper_lid_y,
             "UPPER_LID_ANGLE": upper_lid_angle,
             "UPPER_LID_BEND": upper_lid_bend,
            },
            {
             "CENTER_Y": center_y,
             "UPPER_LID_Y": upper_lid_y,
             "UPPER_LID_ANGLE": -upper_lid_angle,
             "UPPER_LID_BEND": upper_lid_bend,
            })


class DisappointedFace(Face):
    """
    Function to produce a disappointed face.

    Standard face is DisappointedFace(0.3, 5.0, 0.4)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_lid_y=0.3, upper_lid_angle=10.0, lower_lid_y=0.4):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            })


class EmbarrassedFace(Face):
    """
    Function to produce an embarrassed face.

    Standard face is EmbarrassedFace(0.5, 10.0, 0.2, 0.1)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    UPPER_LID_BEND = (0.0, 0.0, 1.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_lid_y=0.5, upper_lid_angle=10.0, upper_lid_bend=0.2, lower_lid_y=0.1):
        super().__init__(
            {
             "UPPER_LID_Y": upper_lid_y,
             "UPPER_LID_ANGLE": upper_lid_angle,
             "UPPER_LID_BEND": upper_lid_bend,
             "LOWER_LID_Y": lower_lid_y
            },
            {
             "UPPER_LID_Y": upper_lid_y,
             "UPPER_LID_ANGLE": -upper_lid_angle,
             "UPPER_LID_BEND": upper_lid_bend,
             "LOWER_LID_Y": lower_lid_y
            })


# Sub-face of disgust.
class HorrifiedFace(Face):
    """
    Function to produce a horrified face.

    Standard face is HorrifiedFace(30.0)

    UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_angle=20.0, lower_lid_y=0.5):
        super().__init__(
            {
             "UPPER_LID_ANGLE": upper_lid_angle,
            },
            {
             "UPPER_LID_ANGLE": -upper_lid_angle,
            })


# Sub-faces of anger.
# Skeptical is similar to perplexed.
class SkepticalFace(Face):
    """
    Function to produce a skeptical face.

    Standard face is SkepticalFace(left_eye=(0.4, 10.0), right_eye=(0.15, 25.0))

    UPPER_LID_Y: (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, left_eye=(0.4, 10.0), right_eye=(0.15, 25.0)):
        super().__init__(
            {
                "UPPER_LID_Y": left_eye[0],
                "UPPER_LID_ANGLE": -left_eye[1]
            },
            {
                "UPPER_LID_Y": right_eye[0],
                "UPPER_LID_ANGLE": right_eye[1]
            })


class AnnoyedFace(Face):
    """
    Function to produce an annoyed face.

    Standard face is AnnoyedFace(left_eye=(30.0, 0.3, 10.0), right_eye=(1.0, 1.0, 0.2, 30.0, 0.4, 5.0))

    LEFT EYE PARAMETERS:
    UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0)

    RIGHT EYE PARAMETERS:
    UPPER_INNER_RADIUS_X = (0.5, 0.0, 1.0); UPPER_OUTER_RADIUS_X = (0.5, 0.0, 1.0);
    UPPER_LID_Y: (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y: (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0)
    """
    def __init__(self, left_eye=(30.0, 0.3, 10.0), right_eye=(1.0, 1.0, 0.2, 30.0, 0.4, 5.0)):
        super().__init__(
            {
                "UPPER_LID_ANGLE": -left_eye[0],
                "LOWER_LID_Y": left_eye[1],
                "LOWER_LID_ANGLE": -left_eye[2]
            },
            {
                "UPPER_INNER_RADIUS_X": right_eye[0],
                "UPPER_OUTER_RADIUS_X": right_eye[1],
                "UPPER_LID_Y": right_eye[2],
                "UPPER_LID_ANGLE": right_eye[3],
                "LOWER_LID_Y": right_eye[4],
                "LOWER_LID_ANGLE": right_eye[5]
            })


# Also known as enraged
class FuriousFace(Face):
    """
    Function to produce a furious face.

    Standard face is FuriousFace(0.4, 5.0, 0.5)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_lid_y=0.3, upper_lid_angle=30.0, lower_lid_y=0.4):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            })


class SuspiciousFace(Face):
    """
    Function to produce a suspicious face.

    Standard face is SuspiciousFace(0.4, 10.0, 0.5)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_lid_y=0.4, upper_lid_angle=10.0, lower_lid_y=0.5):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            })


# Taken from "withdrawn"
class RejectedFace(Face):
    """
    Function to produce a rejected face.

    Standard face is RejectedFace(0.8, 25.0)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    """
    def __init__(self, upper_lid_y=0.8, upper_lid_angle=25.0):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
            })


# Sub-faces of "bad" emotions
class BoredFace(Face):
    """
    Function to produce a bored face.

    Standard face is BoredFace(0.4)

    UPPER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_lid_y=0.4):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
            })


class TiredFace(Face):
    """
    Function to produce a tired face.

    Standard face is TiredFace(0.4, 5.0, 0.5)

    UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, upper_lid_y=0.4, upper_lid_angle=5.0, lower_lid_y=0.5):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": -upper_lid_angle,
                "LOWER_LID_Y": lower_lid_y,
            })


class AsleepFace(Face):
    """
    Function to produce an asleep face.

    Standard face is AsleepFace(50, 0.5, 0.5)

    CENTER_Y = (0, -50, 50);
    UPPER_LID_Y = (0.0, 0.0, 1.0);
    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, center_y=50, upper_lid_y=0.5, lower_lid_y=0.5):
        super().__init__(
            {
                "CENTER_Y": center_y,
                "UPPER_LID_Y": upper_lid_y,
                "LOWER_LID_Y": lower_lid_y,
            },
            {
                "CENTER_Y": center_y,
                "UPPER_LID_Y": upper_lid_y,
                "LOWER_LID_Y": lower_lid_y,
            })


# Sub-faces of surprise.
class ConfusedFace(Face):
    """
    Function to produce a confused face.

    Standard face is ConfusedFace(left_eye=(), right_eye=())

    LEFT EYE PARAMETERS:
    LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_BEND = = (0.0, 0.0, 1.0);

    RIGHT EYE PARAMETERS:
    UPPER_LID_Y: (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y: (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0); LOWER_LID_BEND = = (0.0, 0.0, 1.0);
    """
    def __init__(self, left_eye=(0.2, 0.2), right_eye=(0.3, 10.0, 0.2, 5.0, 0.2)):
        super().__init__(
            {
                "LOWER_LID_Y": left_eye[0],
                "LOWER_LID_BEND": left_eye[1]
            },
            {
                "UPPER_LID_Y": right_eye[0],
                "UPPER_LID_ANGLE": -right_eye[1],
                "LOWER_LID_Y": right_eye[2],
                "LOWER_LID_ANGLE": right_eye[3],
                "LOWER_LID_BEND": right_eye[4]
            })


class AmazedFace(Face):
    """
    Function to produce an amazed face.

    Standard face is AmazedFace()

    LOWER_LID_Y = (0.0, 0.0, 1.0);
    """
    def __init__(self, lower_lid_y=0.2):
        super().__init__(
            {
                "LOWER_LID_Y": lower_lid_y
            },
            {
                "LOWER_LID_Y": lower_lid_y
            })


class ExcitedFace(Face):
    """
    Function to produce an excited face.

    Standard face is ExcitedFace()

    LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_BEND = (0.0, 0.0, 1.0);
    """
    def __init__(self, lower_lid_y=0.3, lower_lid_bend=0.2):
        super().__init__(
            {
                "LOWER_LID_Y": lower_lid_y,
                "LOWER_LID_BEND": lower_lid_bend
            },
            {
                "LOWER_LID_Y": lower_lid_y,
                "LOWER_LID_BEND": lower_lid_bend
            })


class BlinkLow(Face):
    """
    Function to produce a low blink.
    """
    def __init__(self, upper_lid_y=1.1):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
            })


class BlinkHigh(Face):
    """
    Function to produce a high blink.
    """
    def __init__(self, center_y=-50, upper_lid_y=0.6, lower_lid_y=0.6):
        super().__init__(
            {
                "CENTER_Y": center_y,
                "UPPER_LID_Y": upper_lid_y,
                "LOWER_LID_Y": lower_lid_y
            },
            {
                "CENTER_Y": center_y,
                "UPPER_LID_Y": upper_lid_y,
                "LOWER_LID_Y": lower_lid_y
            })


class BlinkMed(Face):
    """
    Function to produce a middle blink.
    """
    def __init__(self, upper_lid_y=0.6, lower_lid_y=0.6):
        super().__init__(
            {
                "UPPER_LID_Y": upper_lid_y,
                "LOWER_LID_Y": lower_lid_y
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "LOWER_LID_Y": lower_lid_y
            })


def interpolation(prior_face, next_face, alpha):
    temp_face = prior_face.interpolateface(next_face, alpha)
    face_render = np.array(temp_face.render())
    large = cv2.resize(face_render, (width, height), interpolation=cv2.INTER_NEAREST)
    return cv2.imshow("Face", large)

def get_next_frame(prior_face, interpolation_speed, event):

    int_speed = {
        0: 70,  # NeutralFace(),
        1: 70,  # HappyFace(),
        2: 70,  # AmazedFace(),
        3: 70,  # ExcitedFace(),
        4: 70,  # AngryFace(),
        5: 70,  # SurprisedFace(),
        6: 70,  # FearFace(),
        7: 70,  # DespairFace(),
        8: 70,  # DisappointedFace(),
        9: 70,  # EmbarrassedFace(),
        10: 70,  # HorrifiedFace(),
        11: 70,  # AnnoyedFace(),
        12: 70,  # FuriousFace(),
        13: 70,  # DisgustFace(),
        14: 70,  # PleadingFace(),
        15: 70,  # GuiltyFace(),
        16: 70,  # SkepticalFace(),
        17: 70,  # SuspiciousFace(),
        18: 70,  # ConfusedFace(),
        19: 70,  # SadFace(),
        20: 70,  # VulnerableFace(),
        21: 70,  # RejectedFace(),
        22: 70,  # BoredFace(),
        23: 70,  # TiredFace(),
        24: 70  # AsleepFace()
    }
    blink_height = {
        0: BlinkMed(),  # NeutralFace(),
        1: BlinkHigh(),  # HappyFace(),
        2: BlinkMed(),  # AmazedFace(),
        3: BlinkMed(),  # ExcitedFace(),
        4: BlinkLow(),  # AngryFace(),
        5: BlinkMed(),  # SurprisedFace(),
        6: BlinkMed(),  # FearFace(),
        7: BlinkLow(),  # DespairFace(),
        8: BlinkMed(),  # DisappointedFace(),
        9: BlinkLow(),  # EmbarrassedFace(),
        10: BlinkMed(),  # HorrifiedFace(),
        11: BlinkMed(),  # AnnoyedFace(),
        12: BlinkMed(),  # FuriousFace(),
        13: BlinkMed(),  # DisgustFace(),
        14: BlinkMed(),  # PleadingFace(),
        15: BlinkLow(),  # GuiltyFace(),
        16: BlinkLow(),  # SkepticalFace(),
        17: BlinkMed(),  # SuspiciousFace(),
        18: BlinkMed(),  # ConfusedFace(),
        19: BlinkLow(),  # SadFace(),
        20: BlinkMed(),  # VulnerableFace(),
        21: BlinkLow(),  # RejectedFace(),
        22: BlinkLow(),  # BoredFace(),
        23: BlinkMed(),  # TiredFace(),
        24: BlinkLow()  # AsleepFace()
    }
    face_type = {
        0: NeutralFace(),
        # High arousal high valence
        1: HappyFace(),
        2: AmazedFace(),
        3: ExcitedFace(),
        # High arousal low valence
        4: AngryFace(),
        5: SurprisedFace(),
        6: FearFace(),
        7: DespairFace(),
        8: DisappointedFace(),
        9: EmbarrassedFace(),
        10: HorrifiedFace(),
        11: AnnoyedFace(),
        12: FuriousFace(),
        # Med arousal low valence
        13: DisgustFace(),
        14: PleadingFace(),
        15: GuiltyFace(),
        16: SkepticalFace(),
        17: SuspiciousFace(),
        18: ConfusedFace(),
        # Low arousal low valence
        19: SadFace(),
        20: VulnerableFace(),
        21: RejectedFace(),
        22: BoredFace(),
        23: TiredFace(),
        24: AsleepFace()
    }
    blink_int_time = {
        0: 6000,  # NeutralFace(),
        1: 6000,  # HappyFace(),
        2: 6000,  # AmazedFace(),
        3: 6000,  # ExcitedFace(),
        4: 6000,  # AngryFace(),
        5: 6000,  # SurprisedFace(),
        6: 6000,  # FearFace(),
        7: 6000,  # DespairFace(),
        8: 6000,  # DisappointedFace(),
        9: 6000,  # EmbarrassedFace(),
        10: 6000,  # HorrifiedFace(),
        11: 6000,  # AnnoyedFace(),
        12: 6000,  # FuriousFace(),
        13: 6000,  # DisgustFace(),
        14: 6000,  # PleadingFace(),
        15: 6000,  # GuiltyFace(),
        16: 6000,  # SkepticalFace(),
        17: 6000,  # SuspiciousFace(),
        18: 6000,  # ConfusedFace(),
        19: 6000,  # SadFace(),
        20: 6000,  # VulnerableFace(),
        21: 6000,  # RejectedFace(),
        22: 6000,  # BoredFace(),
        23: 6000,  # TiredFace(),
        24: 6000  # AsleepFace()
    }

    next_face = face_type[event]
    for alpha in np.arange(0, 1, interpolation_speed):
        interpolation(prior_face, next_face, alpha)
        cv2.waitKey(50)
    interpolation_speed = int_speed[event]
    blink_height = blink_height[event]
    blink_int_time = blink_int_time[event]

    return next_face, interpolation_speed, blink_height, blink_int_time

def display_all_faces():
    face_type = {
        0: NeutralFace(),
        # High arousal high valence
        1: HappyFace(),
        2: AmazedFace(),
        3: ExcitedFace(),
        # High arousal low valence
        4: AngryFace(),
        5: SurprisedFace(),
        6: FearFace(),
        7: DespairFace(),
        8: DisappointedFace(),
        9: EmbarrassedFace(),
        10: HorrifiedFace(),
        11: AnnoyedFace(),
        12: FuriousFace(),
        # Med arousal low valence
        13: DisgustFace(),
        14: PleadingFace(),
        15: GuiltyFace(),
        16: SkepticalFace(),
        17: SuspiciousFace(),
        18: ConfusedFace(),
        # Low arousal low valence
        19: SadFace(),
        20: VulnerableFace(),
        21: RejectedFace(),
        22: BoredFace(),
        23: TiredFace(),
        24: AsleepFace()
    }
    face_name = {
        0: "Neutral",
        1: "Happy",
        2: "Amazed",
        3: "Excited",
        4: "Angry",
        5: "Surprised",
        6: "Fear",
        7: "Despair",
        8: "Disappointed",
        9: "Embarrassed",
        10: "Horrified",
        11: "Annoyed",
        12: "Furious",
        13: "Disgust",
        14: "Pleading",
        15: "Guilty",
        16: "Skeptical",
        17: "Suspicious",
        18: "Confused",
        19: "Sad",
        20: "Vulnerable",
        21: "Rejected",
        22: "Bored",
        23: "Tired",
        24: "Asleep"
    }
    face_render = []
    for i in face_type.keys():
        face_render.append(np.array(face_type[i].render()))
        large = cv2.resize(face_render[i], (20, 20), interpolation=cv2.INTER_NEAREST)
        cv2.imshow(face_name[i], large)
        cv2.waitKey(100)
        while i == 24:
            wait_key = cv2.waitKey(0)
            if wait_key == 27:
                cv2.destroyAllWindows()
                exit(0)

def main():
    display_all_faces()


if __name__ == '__main__':
    main()
