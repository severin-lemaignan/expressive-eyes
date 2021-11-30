"""

Facial expression definitions.

Based on the "Expressive Eyes" project by Catherine Chambers:
https://git.brl.ac.uk/ca2-chambers/expressive-eyes

"""

from typing import Optional, List

from .procedural_face import ProceduralFace, DEFAULT_WIDTH, DEFAULT_HEIGHT


# see Circumplex model
# -1.0 <= arousal <= 1.0
# -1.0 <= valence <= 1.0
AROUSAL_VALENCE = {
    "Neutral": [0.0, 0.0],
    "Anger": [0.9, -0.6],
    "Sadness": [-0.9, -0.2],
    "Happy": [0.0, 0.4],
    "Surprise": [1.0, 0.0],
    "Disgust": [0.5, -0.6],
    "Fear": [0.8, -0.5],
    "Pleading": [-0.4, -0.4],
    "Vulnerability": [-0.6, -0.3],
    "Despair": [-0.55, -0.7],
    "Guilt": [-0.3, -0.5],
    "Disappointment": [-0.1, -0.9],
    "Embarrassment": [-0.6, -0.2],
    "Horror": [-0.2, -1.0],
    "Skepticism": [0.2, -0.2],
    "Annoyance": [-0.2, -0.2],
    "Fury": [1.0, -1.0],
    "Suspicion": [0.2, -0.5],
    "Rejection": [-0.2, -0.9],
    "Boredom": [0.0, -0.2],
    "Tired": [-1.0, 0.0],
    "Asleep": [-1.0, 0.0],
    "Confused": [-0.2, 0.0],
    "Amazed": [0.3, 0.6],
    "Excited": [0.6, 0.6],
}


def get(name):
    """Returns an instance of a face expression.

    for example: expression = get("Happy")
    """
    import sys

    current_module = sys.modules[__name__]
    return getattr(current_module, name)()


def get_valence_arousal(valence=0.0, arousal=0.0):
    """Returns a face expression that best match a pair (valence, arousal)."""
    best_match = ""
    best_distance = 2.0

    for expr, va in AROUSAL_VALENCE.items():
        v, a = va
        distance = (v - valence) * (v - valence) + (a - arousal) * (a - arousal)
        if distance == 0:
            best_match = expr
            break
        if distance < best_distance:
            best_distance = distance
            best_match = expr

    import sys

    current_module = sys.modules[__name__]
    return getattr(current_module, best_match)()


class Neutral(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].scale_x = 0.8
        self.eyes[0].scale_y = 0.8
        self.eyes[1].scale_x = 0.8
        self.eyes[1].scale_y = 0.8


# Six universal expressions by Ekman - https://en.wikipedia.org/wiki/Facial_expression


class Anger(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.6
        self.eyes[0].lids[0].angle = -30.0
        self.eyes[1].lids[0].y = 0.6
        self.eyes[1].lids[0].angle = 30.0


class Sadness(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.6
        self.eyes[0].lids[0].angle = 20.0
        self.eyes[1].lids[0].y = 0.6
        self.eyes[1].lids[0].angle = -20.0


class Happy(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].upper_outer_radius_x = 1.0
        self.eyes[0].upper_inner_radius_x = 1.0
        self.eyes[0].lids[1].y = 0.4
        self.eyes[0].lids[1].bend = 0.4
        self.eyes[1].upper_outer_radius_x = 1.0
        self.eyes[1].upper_inner_radius_x = 1.0
        self.eyes[1].lids[1].y = 0.4
        self.eyes[1].lids[1].bend = 0.4


class Surprise(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].scale_x = 1.25
        self.eyes[0].scale_y = 1.25
        self.eyes[1].scale_x = 1.25
        self.eyes[1].scale_y = 1.25


class Disgust(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[0].angle = 10.0
        self.eyes[0].lids[1].y = 0.3
        self.eyes[1].lids[0].y = 0.2
        self.eyes[1].lids[0].angle = 20.0
        self.eyes[1].lids[1].y = 0.2
        self.eyes[1].lids[1].angle = 10.0


class Fear(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 30.0
        self.eyes[0].lids[0].bend = 0.1
        self.eyes[0].lids[1].y = 0.4
        self.eyes[0].lids[1].angle = 10.0
        self.eyes[1].lids[0].angle = -30.0
        self.eyes[1].lids[0].bend = 0.1
        self.eyes[1].lids[1].y = 0.4
        self.eyes[1].lids[1].angle = -10.0


# Sub-expressions of sadness.


class Pleading(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 30.0
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = -30.0
        self.eyes[1].lids[1].y = 0.5


class Vulnerability(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 20.0
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[1].angle = 10.0
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = -20.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].angle = -10.0
        self.eyes[1].lids[1].y = 0.5


class Despair(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 30.0
        self.eyes[0].lids[0].y = 0.6
        self.eyes[1].lids[0].angle = -30.0
        self.eyes[1].lids[0].y = 0.6


class Guilt(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 10.0
        self.eyes[0].lids[0].y = 0.6
        self.eyes[0].lids[0].bend = 0.3
        self.eyes[1].lids[0].angle = -10.0
        self.eyes[1].lids[0].y = 0.6
        self.eyes[1].lids[0].bend = 0.3


class Disappointment(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -10.0
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[1].y = 0.4
        self.eyes[1].lids[0].angle = 10.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].y = 0.4


class Embarrassment(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 10.0
        self.eyes[0].lids[0].y = 0.5
        self.eyes[0].lids[0].bend = 0.1
        self.eyes[0].lids[1].y = 0.1
        self.eyes[1].lids[0].angle = -10.0
        self.eyes[1].lids[0].y = 0.5
        self.eyes[1].lids[0].bend = 0.1
        self.eyes[1].lids[1].y = 0.1


# Sub-expressions of disgust.


class Horror(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 20.0
        self.eyes[1].lids[0].angle = -20.0


# Sub-expressions of anger.


class Skepticism(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -10.0
        self.eyes[0].lids[0].y = 0.4
        self.eyes[1].lids[0].angle = 25.0
        self.eyes[1].lids[0].y = 0.15


class Annoyance(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -30.0
        self.eyes[0].lids[1].angle = -10.0
        self.eyes[0].lids[1].y = 0.3
        self.eyes[1].lids[0].angle = 30.0
        self.eyes[1].lids[0].y = 0.2
        self.eyes[1].lids[1].angle = 5.0
        self.eyes[1].lids[1].y = 0.4
        self.eyes[1].upper_inner_radius_x = 1.0
        self.eyes[1].upper_outer_radius_x = 1.0


class Fury(ProceduralFace):
    """aka "enragement"."""

    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -30.0
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[1].y = 0.4
        self.eyes[1].lids[0].angle = 30.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].y = 0.4


class Suspicion(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -10.0
        self.eyes[0].lids[0].y = 0.4
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = 10.0
        self.eyes[1].lids[0].y = 0.4
        self.eyes[1].lids[1].y = 0.5


class Rejection(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 25.0
        self.eyes[0].lids[0].y = 0.8
        self.eyes[1].lids[0].angle = 25.0
        self.eyes[1].lids[0].y = 0.8


# Sub expressions of negative emotions.


class Boredom(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.4
        self.eyes[1].lids[0].y = 0.4


class Tired(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 5.0
        self.eyes[0].lids[0].y = 0.4
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = -5.0
        self.eyes[1].lids[0].y = 0.4
        self.eyes[1].lids[1].y = 0.5


class Asleep(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].center_y = 50.0
        self.eyes[0].lids[0].y = 0.45
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].center_y = 50.0
        self.eyes[1].lids[0].y = 0.45
        self.eyes[1].lids[1].y = 0.5


# Sub-expressions of confusion.


class Confused(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[1].y = 0.2
        self.eyes[0].lids[1].bend = 0.2
        self.eyes[1].lids[0].angle = -10.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].angle = 5.0
        self.eyes[1].lids[1].y = 0.2
        self.eyes[1].lids[1].bend = 0.2


class Amazed(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[1].y = 0.2
        self.eyes[1].lids[1].y = 0.2


class Excited(ProceduralFace):
    def __init__(
        self,
        params: Optional[List[float]] = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ):
        super().__init__(params, width, height)
        self.eyes[0].lids[1].y = 0.3
        self.eyes[0].lids[1].bend = 0.2
        self.eyes[1].lids[1].y = 0.3
        self.eyes[1].lids[1].bend = 0.2
