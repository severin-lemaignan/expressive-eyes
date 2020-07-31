from .faces import *
import numpy as np


class FaceManager:

    def __init__(self, width=128, height=64):

        self.face_type = {
            # Event: face, blink_height, blink_time, interpolation_speed
            0: [NeutralFace(), BlinkMed(), 6000, 40],
            1: [HappyFace(), BlinkHigh(), 6000, 40],
            2: [AmazedFace(), BlinkMed(), 6000, 40],
            3: [ExcitedFace(), BlinkMed(), 6000, 40],
            4: [AngryFace(), BlinkLow(), 6000, 40],
            5: [SurprisedFace(), BlinkMed(), 6000, 40],
            6: [FearFace(), BlinkMed(), 6000, 40],
            7: [DespairFace(), BlinkLow(), 6000, 40],
            8: [DisappointedFace(), BlinkMed(), 6000, 40],
            9: [EmbarrassedFace(), BlinkLow(), 6000, 40],
            10: [HorrifiedFace(), BlinkMed(), 6000, 40],
            11: [AnnoyedFace(), BlinkMed(), 6000, 40],
            12: [FuriousFace(), BlinkMed(), 6000, 40],
            13: [DisgustFace(), BlinkMed(), 6000, 40],
            14: [PleadingFace(), BlinkMed(), 6000, 40],
            15: [GuiltyFace(), BlinkLow(), 6000, 40],
            16: [SkepticalFace(), BlinkLow(), 6000, 40],
            17: [SuspiciousFace(), BlinkMed(), 6000, 40],
            18: [ConfusedFace(), BlinkMed(), 6000, 40],
            19: [SadFace(), BlinkLow(), 6000, 40],
            20: [VulnerableFace(), BlinkMed(), 6000, 40],
            21: [RejectedFace(), BlinkLow(), 6000, 40],
            22: [BoredFace(), BlinkLow(), 6000, 40],
            23: [TiredFace(), BlinkLow(), 6000, 40],
            24: [AsleepFace(), BlinkMed(), 6000, 40]
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
        self.is_blinking = False
        self.startup = False

        self.next_expression = None
        self.is_showing_expression = False

        self.prior_face, self.blink_height, self.blink_time, self.interpolation_speed = self.face_type[0]

        self.next_face = self.prior_face
        self.duration = 0

        self.const_interpolation_duration = 6000  # ms
        self.time_elapsed_since_beginning_of_interpolation = 0
        self.frames = 0
        self.blink_down = True

    def get_next_frame(self, event, elapsed_time_since_last_call):

        self.duration = elapsed_time_since_last_call
        self.time += self.duration

        if self.startup is False:
            self.frames = self.time_elapsed_since_beginning_of_interpolation/self.blink_time
            if self.frames > 1:
                self.time_elapsed_since_beginning_of_interpolation = 0
                self.startup = True
                return self.interpolation(self.blink_height, self.next_face, 1.0, self.width, self.height)
            else:
                self.time_elapsed_since_beginning_of_interpolation += self.duration  # ms
                return self.interpolation(self.blink_height, self.next_face, self.frames, self.width, self.height)

        if self.time - self.time_last_blink > self.blink_time:
            self.frames = self.time_elapsed_since_beginning_of_interpolation/self.blink_time
            if self.blink_down:
                if self.frames > 1:
                    self.time_elapsed_since_beginning_of_interpolation = 0
                    self.blink_down = False
                    return self.interpolation(self.next_face, self.blink_height, 1.0, self.width, self.height)
                else:
                    self.time_elapsed_since_beginning_of_interpolation += self.duration
                    return self.interpolation(self.next_face, self.blink_height, self.frames, self.width, self.height)
            else:
                if self.frames > 1:
                    self.time_elapsed_since_beginning_of_interpolation = 0
                    self.blink_down = True
                    self.time_last_blink = self.time
                    return self.interpolation(self.blink_height, self.next_face, 1.0, self.width, self.height)
                else:
                    self.time_elapsed_since_beginning_of_interpolation += self.duration
                    return self.interpolation(self.blink_height, self.next_face, self.frames, self.width, self.height)

        if self.next_expression is None:
            self.prior_face = self.next_face
            self.next_face, self.blink_height, self.blink_time, self.interpolation_speed = self.face_type[event]
            self.next_expression = not None

        if self.next_expression is not None:
            if self.frames > 1:
                self.time_elapsed_since_beginning_of_interpolation = 0
                self.next_expression = None
                return self.interpolation(self.prior_face, self.next_face, 1.0, self.width, self.height)
            else:
                self.time_elapsed_since_beginning_of_interpolation += self.duration
                return self.interpolation(self.prior_face, self.next_face, self.frames, self.width, self.height)

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
