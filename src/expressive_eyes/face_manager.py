from .faces import *
import numpy as np


class FaceManager:

    def __init__(self, width=600, height=480):

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
            18: [ConfusedFace(),BlinkMed(), 6000, 40],
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
        self.startup = True

        self.next_expression = None
        self.is_showing_expression = False

        self.prior_face, self.blink_height, self.blink_time, self.interpolation_speed = self.face_type[0]

        self.next_face = self.prior_face
        self.duration = 0

    def get_next_frame(self, event, elapsed_time_since_last_call):
        self.duration = duration
        self.time += self.duration
        print(self.time - self.time_last_blink)

        if self.startup:
            print("Start up")

            
            # WHEN STARTING:
            # const interpolation_duration = 1.2s
            # time_elapsed_since_begining_of_interpolation = 0


            # AT EACH LOOP (get_next_frame):
            time_elapsed_since_begining_of_interpolation += duration

            alpha = time_elapsed_since_begining_of_interpolation/interpolation_duration
            if alpha > 1: # interpolation finished
                self.face = self.next_face
                return self.face
            else:
                return self.interpolation(self.blink_height, self.next_face, alpha)

            #for alpha in np.arange(0, 1, 0.1):
            #    yield self.interpolation(self.blink_height, self.next_face, alpha)
                #cv2.waitKey(self.interpolation_speed)
            self.startup = False

        if self.time - self.time_last_blink > self.blink_time:  # Blink if time since last blink > self.blink_time (6000ms)
            print("Blinking")
            for alpha in np.arange(0, 1, 0.1):
                yield self.interpolation(self.next_face, self.blink_height, alpha)
                #cv2.waitKey(self.interpolation_speed)
            for alpha in np.arange(0, 1, 0.1):
                yield self.interpolation(self.blink_height, self.next_face, alpha)
                #cv2.waitKey(self.interpolation_speed)
            self.time_last_blink = self.time

        if self.next_expression is None:
            self.prior_face = self.next_face
            self.next_face, self.blink_height, self.blink_time, self.interpolation_speed = self.face_type[event]
            self.next_expression = not None

        if self.next_expression is not None:
            print("Show expression")
            for alpha in np.arange(0, 1, 0.1):
                #cv2.waitKey(self.interpolation_speed)
                yield self.interpolation(self.prior_face, self.next_face, alpha)
            self.next_expression = None

    def interpolation(self, prior_face, next_face, alpha):
        temp_face = prior_face.interpolateface(next_face, alpha)
        face_render = np.array(temp_face.render())
        resized_image = cv2.resize(face_render, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
        return resized_image

    def show_expression(self, face_str, duration):
        self.next_face = self.face_name[face_str]
        self.duration = duration

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
