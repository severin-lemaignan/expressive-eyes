#!/usr/bin/env python
import pycozmo.procedural_face as pycozmo_face
from scipy import interpolate

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

    def face_render(self, width=128, height=64):
        face = pycozmo_face.ProceduralFace(left_eye=self.left, right_eye=self.right, WIDTH=width, HEIGHT=height)
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
                "UPPER_LID_ANGLE": -upper_lid_angle,
            },
            {
                "UPPER_LID_Y": upper_lid_y,
                "UPPER_LID_ANGLE": upper_lid_angle,
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
    def __init__(self, upper_lid_angle=20.0):
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


def main():
    pass


if __name__ == '__main__':
    main()
