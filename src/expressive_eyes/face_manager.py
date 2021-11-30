from . import expressions as exp
from . import procedural_face as pf


class FaceManager:
    def __init__(self):
        self.current_expression = exp.Neutral()
        self.next_expression = None

        self.ideal_FPS = 200

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

    def step(self, elapsed_time):
        """:param elapsed_time: elapsed time since last call to step, in milliseconds."""

        nb_frames = int(elapsed_time * self.ideal_FPS / 1000.0)

        idx = 0
        for face in self.face_generator:
            if idx == nb_frames:
                self.current_expression = face
                break
            idx += 1

        if idx < nb_frames:  # we are at the end of the interpolation
            self.current_expression = self.next_expression

        return self.current_expression
