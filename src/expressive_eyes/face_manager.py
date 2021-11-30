from itertools import chain

from . import expressions as exp
from . import procedural_face as pf


class FaceManager:

    BLINK_PERIOD = 2000  # milliseconds
    BLINK_SCALE_X = 1
    BLINK_SCALE_Y = 0
    BLINK_STEPS = 10

    def __init__(self):

        self.ideal_FPS = 60

        self.current_expression = exp.Neutral()
        self.next_expression = None

        self.time_since_last_blink = 0
        self.is_interpolating = False

    def set_next_expression(self, expression, duration):
        """Create a face_list array (the number of frames is calculated
        according to the duration time)

        This function takes two variables: expression and duration time. While
        the expression is a procedural face object, duration needs to be given
        as seconds.
        """

        number_of_frames = int(duration * self.ideal_FPS)
        self.next_expression = expression
        self.face_generator = pf.interpolate(
            self.current_expression, self.next_expression, number_of_frames
        )

        self.is_interpolating = True

    def step(self, elapsed_time):
        """:param elapsed_time: elapsed time since last call to step, in milliseconds."""

        nb_frames_to_skip = int(elapsed_time * self.ideal_FPS / 1000.0)
        self.time_since_last_blink += elapsed_time

        if not self.is_interpolating and self.time_since_last_blink > self.BLINK_PERIOD:
            self.face_generator = self.blink()
            self.time_since_last_blink = 0
            self.is_interpolating = True

        idx = 0
        for face in self.face_generator:
            if idx == nb_frames_to_skip:
                self.current_expression = face
                break
            idx += 1

        if (
            self.is_interpolating and idx < nb_frames_to_skip
        ):  # we are at the end of the interpolation
            self.current_expression = self.next_expression
            self.is_interpolating = False
            self.time_since_last_blink = 0

        return self.current_expression

    def blink(self):
        """Generate blink animation."""

        # Create blink face at the position of the current face.
        target_face = pf.ProceduralFace(list(self.current_expression.params))
        target_face.scale_y = self.BLINK_SCALE_Y
        target_face.eyes[0].scale_x = self.BLINK_SCALE_X
        target_face.eyes[1].scale_x = self.BLINK_SCALE_X
        target_face.eyes[0].scale_y = self.BLINK_SCALE_Y
        target_face.eyes[1].scale_y = self.BLINK_SCALE_Y

        part1 = pf.interpolate(self.current_expression, target_face, self.BLINK_STEPS)
        part2 = pf.interpolate(target_face, self.current_expression, self.BLINK_STEPS)

        return chain(part1, part2)
