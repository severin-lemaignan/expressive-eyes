from .faces import *
import numpy as np


class FaceManager:

    def __init__(self, width=128, height=64):

        self.face_type = {
            # Event: face, blink_height, blink_time, interpolation_speed
            0: [NeutralFace(), BlinkMed(), 6000, 4000],
            1: [HappyFace(), BlinkHigh(), 6000, 4000],
            2: [AmazedFace(), BlinkMed(), 6000, 4000],
            3: [ExcitedFace(), BlinkMed(), 6000, 4000],
            4: [AngryFace(), BlinkLow(), 6000, 4000],
            5: [SurprisedFace(), BlinkMed(), 6000, 4000],
            6: [FearFace(), BlinkMed(), 6000, 4000],
            7: [DespairFace(), BlinkLow(), 6000, 4000],
            8: [DisappointedFace(), BlinkMed(), 6000, 4000],
            9: [EmbarrassedFace(), BlinkLow(), 6000, 4000],
            10: [HorrifiedFace(), BlinkMed(), 6000, 4000],
            11: [AnnoyedFace(), BlinkMed(), 6000, 4000],
            12: [FuriousFace(), BlinkMed(), 6000, 4000],
            13: [DisgustFace(), BlinkMed(), 6000, 4000],
            14: [PleadingFace(), BlinkMed(), 6000, 4000],
            15: [GuiltyFace(), BlinkLow(), 6000, 4000],
            16: [SkepticalFace(), BlinkLow(), 6000, 4000],
            17: [SuspiciousFace(), BlinkMed(), 6000, 4000],
            18: [ConfusedFace(), BlinkMed(), 6000, 4000],
            19: [SadFace(), BlinkLow(), 6000, 4000],
            20: [VulnerableFace(), BlinkMed(), 6000, 4000],
            21: [RejectedFace(), BlinkLow(), 6000, 4000],
            22: [BoredFace(), BlinkLow(), 6000, 4000],
            23: [TiredFace(), BlinkLow(), 6000, 4000],
            24: [AsleepFace(), BlinkMed(), 6000, 4000]
        }
        self.face_name = {
            "Neutral": NeutralFace(),
            "Happy": HappyFace(),
            "Amazed": AmazedFace(),
            "Excited": ExcitedFace(),
            "Angry": AngryFace(),
            "Surprised": SurprisedFace(),
            "Fear": FearFace(),
            "Despair": DespairFace(),
            "Disappointed": DisappointedFace(),
            "Embarrassed": EmbarrassedFace(),
            "Horrified": HorrifiedFace(),
            "Annoyed": AnnoyedFace(),
            "Furious": FuriousFace(),
            "Disgust": DisgustFace(),
            "Pleading": PleadingFace(),
            "Guilty": GuiltyFace(),
            "Skeptical": SkepticalFace(),
            "Suspicious": SuspiciousFace(),
            "Confused": ConfusedFace(),
            "Sad": SadFace(),
            "Vulnerable": VulnerableFace(),
            "Rejected": RejectedFace(),
            "Bored": BoredFace(),
            "Tired": TiredFace(),
            "Asleep": AsleepFace()
        }

        self.width = width
        self.height = height

        self.time = 0  # in ms
        self.time_last_blink = 0
        self.duration = 0

        self.startup = False
        self.blink_down = True
        self.next_expression = None

        self.prior_face, self.blink_height, self.blink_time, self.interpolation_speed = self.face_type[0]

        self.next_face = self.prior_face

        self.time_elapsed_since_beginning_of_interpolation = 0
        self.frames = 0
        self.wait_time = 0

    def run_expressive_eyes(self, event, elapsed_time_since_last_call):
        self.wait_time = elapsed_time_since_last_call
        self.duration = elapsed_time_since_last_call
        self.time += self.duration

        if self.startup is False:  # Startup
            face, self.wait_time, self.startup = self.get_next_frame(self.blink_time, self.startup, self.blink_height, self.next_face)
            return face, self.wait_time

        if self.time - self.time_last_blink > self.blink_time:  # Blinking
            if self.blink_down:  # Blinking down
                face, self.wait_time, self.blink_down = self.get_next_frame(self.blink_time, self.blink_down, self.next_face, self.blink_height)
                return face, self.wait_time
            else:  # Blinking up
                face, self.wait_time, self.blink_down = self.get_next_frame(self.blink_time, self.blink_down, self.blink_height, self.next_face)
                if self.blink_down:
                    self.time_last_blink = self.time
                    return face, self.wait_time
                else:
                    return face, self.wait_time

        if self.next_expression is None:  # Setting the next expression
            self.prior_face = self.next_face
            self.next_face, self.blink_height, self.blink_time, self.interpolation_speed = self.face_type[event]
            self.next_expression = not None

        if self.next_expression is not None:  # Displaying the next expression
            if self.prior_face == self.next_face:
                self.wait_time = 1
                return self.interpolation(self.prior_face, self.next_face, 1.0, self.width, self.height), self.wait_time
            else:
                face, self.wait_time, _ = self.get_next_frame(self.interpolation_speed, None, self.prior_face, self.next_face,)
                return face, self.wait_time

    def get_next_frame(self, interpolation_time, true_statement, prior_face, next_face):
        self.frames = self.time_elapsed_since_beginning_of_interpolation/interpolation_time
        if self.frames == 0:
            self.wait_time = 1/(self.duration/interpolation_time)
        else:
            self.wait_time = max(1, int(1/self.frames))
        if self.frames > 1:
            self.time_elapsed_since_beginning_of_interpolation = 0
            return self.interpolation(prior_face, next_face, 1.0, self.width, self.height), self.wait_time, not true_statement
        else:
            self.time_elapsed_since_beginning_of_interpolation += self.duration
            return self.interpolation(prior_face, next_face, self.frames, self.width, self.height), self.wait_time, true_statement

    @staticmethod
    def interpolation(prior_face, next_face, alpha, width, height):
        temp_face = prior_face.interpolateface(next_face, alpha)
        face_render = np.array(temp_face.face_render(width=width, height=height))
        return face_render

    def show_expression(self, face_str, duration):
        self.next_face = self.face_name[face_str]
        self.duration = duration

    def display_all_faces(self):
        face_show = []
        for name, face in self.face_name.items():
            face_show.append(np.array(face.face_render()))
            cv2.imshow(name, face_show)
