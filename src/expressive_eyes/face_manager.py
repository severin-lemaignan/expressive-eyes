from faces import *
import numpy as np


class FaceManager:

    def __init__(self, width=128, height=64):
        self.face_type = {
            # face face_type, blink_height, blink_time, const_interpolation_time (seconds)
            "Neutral": [NeutralFace(), BlinkMed(), 6, 1],
            "Happy": [HappyFace(), BlinkHigh(), 6, 1],
            "Amazed": [AmazedFace(), BlinkMed(), 6, 1],
            "Excited": [ExcitedFace(), BlinkMed(), 6, 1],
            "Angry": [AngryFace(), BlinkLow(), 6, 1],
            "Surprised": [SurprisedFace(), BlinkMed(), 6, 1],
            "Fear": [FearFace(), BlinkMed(), 6, 1],
            "Despair": [DespairFace(), BlinkLow(), 6, 1],
            "Disappointed": [DisappointedFace(), BlinkMed(), 6, 1],
            "Embarrassed": [EmbarrassedFace(), BlinkLow(), 6, 1],
            "Horrified": [HorrifiedFace(), BlinkMed(), 6, 1],
            "Annoyed": [AnnoyedFace(), BlinkMed(), 6, 1],
            "Furious": [FuriousFace(), BlinkMed(), 6, 1],
            "Disgust": [DisgustFace(), BlinkMed(), 6, 1],
            "Pleading": [PleadingFace(), BlinkMed(), 6, 1],
            "Guilty": [GuiltyFace(), BlinkLow(), 6, 1],
            "Skeptical": [SkepticalFace(), BlinkLow(), 6, 1],
            "Suspicious": [SuspiciousFace(), BlinkMed(), 6, 1],
            "Confused": [ConfusedFace(), BlinkMed(), 6, 1],
            "Sad": [SadFace(), BlinkLow(), 6, 1],
            "Vulnerable": [VulnerableFace(), BlinkMed(), 6, 1],
            "Rejected": [RejectedFace(), BlinkLow(), 6, 1],
            "Bored": [BoredFace(), BlinkLow(), 6, 1],
            "Tired": [TiredFace(), BlinkLow(), 6, 1],
            "Asleep": [AsleepFace(), BlinkMed(), 6, 1]
        }

        self.width = width
        self.height = height

        self.startup = True
        self.blink_down = True
        self.next_expression = False

        self.face_str = "Neutral"
        self.prior_face, self.blink_height, self.blink_time, self.const_interpolation_time = self.face_type[self.face_str]

        self.current_face = self.prior_face

        self.frames = 0
        self.time_between_frames = 0
        self.time_last_blink = 0

    def run_expressive_eyes(self, face_str, elapsed_time):
        self.time_between_frames = elapsed_time
        self.face_str = face_str

        if self.startup:
            face, self.startup = self.get_next_frame(self.startup, self.const_interpolation_time, self.blink_height,
                                                     self.current_face)
            return face
        print(elapsed_time)
        self.time_last_blink += elapsed_time

        if self.time_last_blink > self.blink_time:
            if self.blink_down:
                face, self.blink_down = self.get_next_frame(self.blink_down, self.blink_time, self.current_face,
                                                            self.blink_height)
                return face
            else:
                face, self.blink_down = self.get_next_frame(self.blink_down, self.blink_time, self.blink_height,
                                                            self.current_face)
                if self.blink_down:
                    self.time_last_blink = 0
                    return face
                else:
                    return face

        if self.next_expression is False:
            self.eye_position(0, 0, 0)
            self.set_next_expression(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0)
            self.next_expression = True

        if self.next_expression:
            if self.prior_face == self.current_face:
                return self.interpolation(self.prior_face, self.current_face, 1.0, self.width, self.height)
            else:
                face, self.next_expression = self.get_next_frame(self.next_expression, self.const_interpolation_time,
                                                                 self.prior_face, self.current_face)
                return face

    def get_next_frame(self, boolean, interpolation_time, prior_face, current_face):
        self.const_interpolation_time = interpolation_time
        self.frames += self.time_between_frames / self.const_interpolation_time
        if self.frames >= 1:
            self.frames = 0
            return self.interpolation(prior_face, current_face, 1.0, self.width, self.height), not boolean
        else:
            return self.interpolation(prior_face, current_face, self.frames, self.width, self.height), boolean

    def set_next_expression(self, au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23,
                            au25, au26, au28, au45):
        au_names = {
            "inner brow raiser": au01,
            "outer brow raiser": au02,
            "brow lowerer": au04,
            "upper lid raiser": au05,
            "cheek raiser": au06,
            "lid tightener": au07,
            "nose wrinkler": au09,
            "upper lip raiser": au10,
            "lip corner puller": au12,
            "dimpler": au14,
            "lip corner depresser": au15,
            "chin raiser": au17,
            "lip stretcher": au20,
            "lip tightener": au23,
            "lips part": au25,
            "jaw drop": au26,
            "blink": au45
        }
        au_standard_values = {
            "Neutral": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, None],
            "Happy": [0, 0, 0, 1, 1, 0, 1, 1, None, 0, None, 0, 0, 0, 0, 0, None],
            "Amazed": [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 1, 1, 0, None],
            "Excited": [0, 0, 0, 1, 1, 1, 1, 1, None, 0, None, 1, 0, 0, 0, 0, None],
            "Angry": [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, None, 1, 1, 0, 0, 0, None],  # au23 and au24 must be present
            "Surprised": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, None, None, 0, None],  # Either au1+2 or 5 must be
            # present and the intensity of AU5 must not be stronger than B
            "Fear": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None], # AU combination of au1+2+4 must be present, unless au5 is of intensity E then au4 can be absent
            "Despair": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Disappointed": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Embarrassed": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Horrified": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Annoyed": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Furious": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Disgust": [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, None],  # Either au09 or au10 is present
            "Pleading": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Guilty": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Skeptical": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Suspicious": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Confused": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Sad": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, None],
            "Vulnerable": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Rejected": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Bored": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Tired": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None],
            "Asleep": [au02, au04, au05, au06, au07, au09, au10, au12, None, au15, None, au20, au23, au25, au26, au28, None]
        }
        self.prior_face = self.current_face
        self.current_face, self.blink_height, self.blink_time, self.const_interpolation_time = self.face_type[self.face_str]

    def eye_position(self, eye_y, left_eye_x, right_eye_x):
        self.current_face.left[0] = self.blink_height.left[0] = left_eye_x
        self.current_face.right[0] = self.blink_height.right[0] = right_eye_x
        self.current_face.left[1] = self.current_face.right[1] = \
            self.blink_height.left[1] = self.blink_height.right[1] = eye_y

    @staticmethod
    def interpolation(prior_face, current_face, frames, width, height):
        temp_face = prior_face.interpolateface(current_face, frames)
        face_render = np.array(temp_face.face_render(width=width, height=height))
        return face_render

    def display_all_faces(self):
        face_show = []
        face = [item[0:25][0] for item in list(self.face_type.values())]
        name = list(self.face_type.keys())
        for i in range(0, 25):
            face_show.append(np.array(face[i].face_render()))
            cv2.imshow(name[i], face_show[i])
