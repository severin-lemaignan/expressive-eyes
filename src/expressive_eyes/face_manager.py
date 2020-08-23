from faces import *
import numpy as np


class FaceManager:

    def __init__(self, width=128, height=64):
        self.face_type = {
            # face face_type, blink_height, blink_time, const_interpolation_time (seconds)
            "Neutral": [NeutralFace(), BlinkMed(), 6, 1],
            "Happy": [HappyFace(), BlinkHigh(), 6000, 4],
            "Amazed": [AmazedFace(), BlinkMed(), 6000, 4],
            "Excited": [ExcitedFace(), BlinkMed(), 6000, 4],
            "Angry": [AngryFace(), BlinkLow(), 6, 1],
            "Surprised": [SurprisedFace(), BlinkMed(), 6000, 4],
            "Fear": [FearFace(), BlinkMed(), 6000, 4],
            "Despair": [DespairFace(), BlinkLow(), 6000, 4],
            "Disappointed": [DisappointedFace(), BlinkMed(), 6, 4],
            "Embarrassed": [EmbarrassedFace(), BlinkLow(), 6000, 4],
            "Horrified": [HorrifiedFace(), BlinkMed(), 6000, 4],
            "Annoyed": [AnnoyedFace(), BlinkMed(), 6000, 4],
            "Furious": [FuriousFace(), BlinkMed(), 6000, 4],
            "Disgust": [DisgustFace(), BlinkMed(), 6000, 4],
            "Pleading": [PleadingFace(), BlinkMed(), 6000, 4],
            "Guilty": [GuiltyFace(), BlinkLow(), 6000, 4],
            "Skeptical": [SkepticalFace(), BlinkLow(), 6000, 4],
            "Suspicious": [SuspiciousFace(), BlinkMed(), 6000, 4],
            "Confused": [ConfusedFace(), BlinkMed(), 6000, 4],
            "Sad": [SadFace(), BlinkLow(), 6000, 4],
            "Vulnerable": [VulnerableFace(), BlinkMed(), 6000, 4],
            "Rejected": [RejectedFace(), BlinkLow(), 6000, 4],
            "Bored": [BoredFace(), BlinkLow(), 6000, 4],
            "Tired": [TiredFace(), BlinkLow(), 6000, 4],
            "Asleep": [AsleepFace(), BlinkMed(), 6000, 4]
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

        if self.startup:
            face, self.startup = self.get_next_frame(self.startup, self.const_interpolation_time, self.blink_height,
                                                     self.current_face)
            return face

        self.face_str = face_str
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
            self.prior_face = self.current_face
            self.current_face, self.blink_height, self.blink_time, self.const_interpolation_time = self.face_type[self.face_str]
            self.eye_position(0, 0, 0)  # This cannot be static due to dictionary mutability.
            # It sets values for both prior and current face so doesn't interpolate properly if they are the same
            # and the eye_position changes
            self.openface_implementation(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
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

    def openface_implementation(self, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23,
                                au25, au26, au45):
        au_names = {
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
            "Neutral": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Happy": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Amazed": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Excited": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Angry": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Surprised": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Fear": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Despair": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Disappointed": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Embarrassed": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Horrified": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Annoyed": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Furious": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Disgust": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Pleading": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Guilty": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Skeptical": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Suspicious": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Confused": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Sad": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Vulnerable": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Rejected": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Bored": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Tired": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45],
            "Asleep": [au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45]
        }
        face_str = self.face_str
        return face_str

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
