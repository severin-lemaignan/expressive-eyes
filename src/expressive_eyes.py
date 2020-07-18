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


# Smaller than the default eyes so that surprise can be properly expressed (doesn't really work)
class NeutralFace(Face):
    """
    Function to produce the neutral face.

    Standard face is NeutralFace(0.8, 0.8)

    SCALE_X = (1.0, 1.0, 1.0); SCALE_Y = (1.0, 1.0, 1.0);
    """
    def __init__(self, scale_x=0.8, scale_y=0.8):
        super().__init__(
            {
                "SCALE_X": scale_x,
                "SCALE_Y": scale_y,
            },
            {
                "SCALE_X": scale_x,
                "SCALE_Y": scale_y,
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
    def __init__(self, upper_lid_angle=20.0, lower_lid_y=0.5):
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
    pass


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
    def __init__(self, upper_lid_y=0.3, upper_lid_angle=5.0, lower_lid_y=0.4):
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
    pass


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
    UPPER_LID_Y: (0.0, 0.0, 1.0) = UPPER_LID_ANGLE = (0.0, -60.0, 60.0);
    LOWER_LID_Y: (0.0, 0.0, 1.0) = LOWER_LID_ANGLE = (0.0, -60.0, 60.0)
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
    pass


class AmazedFace(Face):
    pass


class ExcitedFace(Face):
    pass


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
        0: 0.1,  # NeutralFace(),
        1: 0.1,  # HappyFace(),
        2: 0.1,  # AmazedFace(),
        3: 0.1,  # ExcitedFace(),
        4: 0.1,  # AngryFace(),
        5: 0.1,  # SurprisedFace(),
        6: 0.1,  # FearFace(),
        7: 0.1,  # DespairFace(),
        8: 0.1,  # DisappointedFace(),
        9: 0.1,  # EmbarrassedFace(),
        10: 0.1,  # HorrifiedFace(),
        11: 0.1,  # AnnoyedFace(),
        12: 0.1,  # FuriousFace(),
        13: 0.1,  # DisgustFace(),
        14: 0.1,  # PleadingFace(),
        15: 0.1,  # GuiltyFace(),
        16: 0.1,  # SkepticalFace(),
        17: 0.1,  # SuspiciousFace(),
        18: 0.1,  # ConfusedFace(),
        19: 0.1,  # SadFace(),
        20: 0.1,  # VulnerableFace(),
        21: 0.1,  # RejectedFace(),
        22: 0.1,  # BoredFace(),
        23: 0.1,  # TiredFace(),
        24: 0.1  # AsleepFace()
    }
    blink_height = {
        0: BlinkMed(),  # NeutralFace(),
        1: BlinkMed(),  # HappyFace(),
        2: BlinkMed(),  # AmazedFace(),
        3: BlinkMed(),  # ExcitedFace(),
        4: BlinkMed(),  # AngryFace(),
        5: BlinkMed(),  # SurprisedFace(),
        6: BlinkMed(),  # FearFace(),
        7: BlinkMed(),  # DespairFace(),
        8: BlinkMed(),  # DisappointedFace(),
        9: BlinkMed(),  # EmbarrassedFace(),
        10: BlinkMed(),  # HorrifiedFace(),
        11: BlinkMed(),  # AnnoyedFace(),
        12: BlinkMed(),  # FuriousFace(),
        13: BlinkMed(),  # DisgustFace(),
        14: BlinkMed(),  # PleadingFace(),
        15: BlinkMed(),  # GuiltyFace(),
        16: BlinkMed(),  # SkepticalFace(),
        17: BlinkMed(),  # SuspiciousFace(),
        18: BlinkMed(),  # ConfusedFace(),
        19: BlinkMed(),  # SadFace(),
        20: BlinkMed(),  # VulnerableFace(),
        21: BlinkMed(),  # RejectedFace(),
        22: BlinkMed(),  # BoredFace(),
        23: BlinkMed(),  # TiredFace(),
        24: None  # AsleepFace()
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

    next_face = face_type[event]
    for alpha in np.arange(0, 1, interpolation_speed):
        interpolation(prior_face, next_face, alpha)
        cv2.waitKey(100)
    interpolation_speed = int_speed[event]
    blink_height = blink_height[event]

    return next_face, interpolation_speed, blink_height


def main():
    face2 = NeutralFace()
    face1 = BlinkHigh()
    for alpha in np.arange(0, 1, 0.1):
        face3 = face2.interpolateface(face1, alpha)
        dst = cv2.medianBlur(np.array(face3.render()),5)
        large = cv2.resize(dst, (width, height), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("image", large)
        cv2.waitKey(100)



if __name__ == '__main__':
    main()
