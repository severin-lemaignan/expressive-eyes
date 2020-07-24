from expressive_eyes import *
import numpy as np


class FaceManager:

    def __init__(self, width=600, height=480):

        self.face_type = {
            # Event: face, blink_height, blink_time, interpolation_speed, key_press
            0: [NeutralFace(), BlinkMed(), 6000, 70, 121],
            1: [HappyFace(), BlinkHigh(), 6000, 70, 97],
            2: [AmazedFace(), BlinkMed(), 6000, 70, 98],
            3: [ExcitedFace(), BlinkMed(), 6000, 70, 99],
            4: [AngryFace(), BlinkLow(), 6000, 70, 100],
            5: [SurprisedFace(), BlinkMed(), 6000, 70, 101],
            6: [FearFace(), BlinkMed(), 6000, 70, 102],
            7: [DespairFace(), BlinkLow(), 6000, 70, 103],
            8: [DisappointedFace(), BlinkMed(), 6000, 70, 104],
            9: [EmbarrassedFace(), BlinkLow(), 6000, 70, 105],
            10: [HorrifiedFace(), BlinkMed(), 6000, 70, 106],
            11: [AnnoyedFace(), BlinkMed(), 6000, 70, 107],
            12: [FuriousFace(), BlinkMed(), 6000, 70, 108],
            13: [DisgustFace(), BlinkMed(), 6000, 70, 109],
            14: [PleadingFace(), BlinkMed(), 6000, 70, 110],
            15: [GuiltyFace(), BlinkLow(), 6000, 70, 111],
            16: [SkepticalFace(), BlinkLow(), 6000, 70, 112],
            17: [SuspiciousFace(), BlinkMed(), 6000, 70, 113],
            18: [ConfusedFace(),BlinkMed(), 6000, 70, 114],
            19: [SadFace(), BlinkLow(), 6000, 70, 115],
            20: [VulnerableFace(), BlinkMed(), 6000, 70, 116],
            21: [RejectedFace(), BlinkLow(), 6000, 70, 117],
            22: [BoredFace(), BlinkLow(), 6000, 70, 118],
            23: [TiredFace(), BlinkLow(), 6000, 70, 119],
            24: [AsleepFace(), BlinkMed(), 6000, 70, 120]
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

        self.next_expression = None
        self.next_expression_duration = 0
        self.time_started_expression = 0
        self.is_showing_expression = False

        self.prior_face = NeutralFace()
        self.next_face = self.prior_face
        self.blink_height = BlinkMed()
        self.blink_time = 6000
        self.interpolation_speed = 70

    def get_next_frame(self, delta, event):

        self.time += delta
        variables = self.face_type[event]
        key = cv2.waitKey(100)

        if key == 27:  # ESC
            cv2.destroyAllWindows()
            exit(0)

        if self.time - self.time_last_blink > 6000:  # Blink if time since last blink > 6000ms
            for alpha in np.arange(0, 1, 0.1):
                self.interpolation(self.next_face, self.blink_height, alpha)
                cv2.waitKey(self.face_type[event[4]])

            for alpha in np.arange(0, 1, 0.1):
                self.interpolation(self.blink_height, self.next_face, alpha)
                cv2.waitKey(self.face_type[event[4]])

            self.time_last_blink = self.time
            self.is_blinking = True

        if self.is_blinking:
            self.blink_time = self.time - self.time_last_blink

        if self.next_expression is None:
            variables = self.face_type[event]
            self.next_face = variables[0]; self.blink_height = variables[1]
            self.blink_time = variables[2]; self.interpolation_speed = variables[3]
            self.prior_face = self.next_face

        if self.next_expression is not None and not self.is_showing_expression:
            for alpha in np.arange(0, 1, 0.1):
                self.interpolation(self.prior_face, self.next_face, alpha)
                cv2.waitKey(self.face_type[event[4]])

            self.time_started_expression = self.time
            self.is_showing_expression = True

        if self.is_showing_expression:
            pass

        return self.next_face

    def interpolation(self, prior_face, next_face, alpha):
        temp_face = prior_face.interpolateface(next_face, alpha)
        face_render = np.array(temp_face.render())
        large = cv2.resize(face_render, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
        return cv2.imshow("Face", large)

    def show_expression(self, face_str, duration):
        self.next_face = self.face_name[face_str]
        self.next_expression_duration = duration

    def display_all_faces(self):
        face_render = []
        for name, face in self.face_name.items():
            i = list(self.face_name.keys()).index(name)
            face_render.append(np.array(face.render()))
            large = cv2.resize(face_render[i], (200, 200), interpolation=cv2.INTER_NEAREST)
            cv2.imshow(name, large)
            cv2.waitKey(100)
            while i == 24:
                wait_key = cv2.waitKey(0)
                if wait_key == 27:
                    cv2.destroyAllWindows()
                    exit(0)
