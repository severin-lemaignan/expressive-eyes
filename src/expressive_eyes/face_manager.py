from .faces import *
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
        self.time_between_blinks = 0

    def run_expressive_eyes(self, face_str, elapsed_time):
        """
        For future programmers: this method decides what should be interpolated. On startup the neutral eyes open. Then the eyes blink, the time taken to interpolate this full blink is given by blink_time. The amount of times the eyes blink per minute is given by time_between_blinks. The next expression is set to the input face_str. Please look at get_next_frame as it is an important part of this method.

        :param face_str: A string describing the desired face. Written as a noun. One of the following: "Neutral" "Happy" "Amazed" "Excited" "Angry" "Surprised" "Fear" "Despair" "Disappointed" "Embarrassed" "Horrified" "Annoyed" "Furious" "Disgust" "Pleading" "Guilty" "Skeptical" "Suspicious" "Confused" "Sad" "Vulnerable" "Rejected" "Bored" "Tired" "Asleep"
        :param elapsed_time: The time taken for the code to run. This changes the time between each frame of interpolation. Also changes the time between blinks. Changing this may have unintended results.
        :return: Popup window displaying expressive eyes. The eyes first open before changing to the face given by face_str
        """
        self.time_between_frames = elapsed_time
        self.face_str = face_str

        if self.startup:
            face, self.startup = self.get_next_frame(self.startup, self.const_interpolation_time, self.blink_height,
                                                     self.current_face)
            return face
        print(elapsed_time)
        self.time_between_blinks += elapsed_time

        if self.time_between_blinks > self.blink_time:
            if self.blink_down:
                face, self.blink_down = self.get_next_frame(self.blink_down, self.blink_time, self.current_face,
                                                            self.blink_height)
                return face
            else:
                face, self.blink_down = self.get_next_frame(self.blink_down, self.blink_time, self.blink_height,
                                                            self.current_face)
                if self.blink_down:
                    self.time_between_blinks = 0
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
        """
        For future programmers: This uses the time_between_frames and constant const_interpolation_time to get the number of frames needed to complete the interpolation in the given time. frames is not the number of frames, but 1/number of frames (this is because you cannot calculate the number of frames directly without dividing by zero on the first loop). Note this returns the rendered face, see FacemMnager.interpolation for the matrix that is used to render the face.

        :param boolean: This boolean is changed from true to false or false to true given on the input. This boolean is used to determine which of the if statements of run_expressive_eyes will run.
        :param interpolation_time: Time taken to interpolate between one face and the next expression. If the next expression is blinking, this time is equal to blink_time. Otherwise this time is fixed and is equal to const_interpolation_time.
        :param prior_face: The face in the prior while loop from demo.py.
        :param current_face: The face in this while loop. This can be inputted as face_str into run_expressive_eyes.
        :return: The interpolated render between the prior face and current face. Also returns the opposite of the input boolean.
        """
        self.const_interpolation_time = interpolation_time
        self.frames += self.time_between_frames / self.const_interpolation_time
        if self.frames >= 1:
            self.frames = 0
            return self.interpolation(prior_face, current_face, 1.0, self.width, self.height), not boolean
        else:
            return self.interpolation(prior_face, current_face, self.frames, self.width, self.height), boolean


    def set_next_expression(self, au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23,
                            au25, au26, au28, au45):
        """
        For the programmer: This code is unfinished. The inputs are the action units detected by openface: https://github.com/TadasBaltrusaitis/OpenFace, https://github.com/TadasBaltrusaitis/OpenFace/wiki/Action-Units. Note that it does not detect all action units, only the ones given below. These action units are intended to be those that detect presence rather than intensity.

        I am not sure that au14 (dimpler) should be an input given that not everyone has dimples and therefore it might be different for different faces pulling the same expression. I left it in because openface provides it as an ouptut.

        All comments in the dictionary au_standard_values are taken from the paper: "The Extended Cohn-Kanade Dataset (CK+): A complete dataset for action unitand emotion-specified expression". They describe the faces from the CK+ database using action units.

        :param au01: inner brow raiser
        :param au02: outer brow raiser
        :param au04: brow lowerer
        :param au05: upper lid raiser
        :param au06: cheek raiser
        :param au07: lid tightener
        :param au09: nose wrinkler
        :param au10: upper lip raiser
        :param au12: lip corner puller
        :param au14: dimpler
        :param au15: lip corner depressor
        :param au17: chin raiser
        :param au20: lip stretcher
        :param au23: lip tightener
        :param au25: lips part
        :param au26: jaw drop
        :param au28: lip suck
        :param au45: blink
        :return: Nothing at the moment, should return a face determined by the given action units
        """
        au_standard_values = {
            "Neutral": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            # For happy: AU12 must be present
            "Happy": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Amazed": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Excited": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            # For angry : AU23 and AU24 must be present in the AU combination
            "Angry": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            # For surprised: Either AU1+2 or 5 must be present and the intensity of AU5 must not be stronger than B
            "Surprised": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            # For fear: AU combination of AU1+2+4 must be present, unless AU5 is of intensity E then AU4 can be absent
            "Fear": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Despair": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Disappointed": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Embarrassed": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Horrified": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Annoyed": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Furious": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            # For disgust: Either AU9 or AU10 must be present
            "Disgust": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Pleading": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Guilty": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Skeptical": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Suspicious": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Confused": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            # For sad: Either AU1+4+15 or 11 must be present. An exception is AU6+15
            "Sad": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Vulnerable": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Rejected": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Bored": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Tired": [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
            "Asleep":  [au01, au02, au04, au05, au06, au07, au09, au10, au12, au14, au15, au17, au20, au23, au25, au26, au28, au45],
        }
        pass

    def eye_position(self, eye_y, left_eye_x, right_eye_x):
        """
        For the programmer: This code is unfinished. Currently you can input a new eye position into this code and it will change the position of both eyes. However, the input should be determined by the position of the user on the webcam (the eyes should look at the user). Also note that I believe because the default face was made using dictionaries this code does not work correctly. Try changing the position of the eyes with face_str = "Neutral" and then with face_str= "Angry" to see what I mean.
        I believe the issue is because changing the position of current_face changes that of the prior_face before interpolation, so when interpolating the eyes appear to jump. Note this only happens if the face_type of the current_face is the same as the prior_face.

        :param eye_y: The y-position of both eyes
        :param left_eye_x: The x-position of the left eye
        :param right_eye_x: The x-position of the right eye
        :return: The current face with the new given positions
        """
        self.current_face.left[0] = self.blink_height.left[0] = left_eye_x
        self.current_face.right[0] = self.blink_height.right[0] = right_eye_x
        self.current_face.left[1] = self.current_face.right[1] = \
            self.blink_height.left[1] = self.blink_height.right[1] = eye_y

    @staticmethod
    def interpolation(prior_face, current_face, frames, width, height):
        """
        Produces a rendered face that is interpolated between prior_face and current_face. The percentage of interpolation is given by frames where 0 means 0% (the prior_face render is the output) and 1 means 100% (the current_face is the output).

        :param prior_face: The face of the prior loop or the face just displayed.
        :param current_face: The face of the current loop or the face about to be displayed.
        :param frames: Equal to 1/(number of frames per interpolation).
        :param width: Width of the output window containing the eyes.
        :param height: Height of the output window containing the eyes.
        :return: The render of the interpolated face. Needs cv2.show to be displayed
        """
        temp_face = prior_face.interpolateface(current_face, frames)
        face_render = np.array(temp_face.face_render(width=width, height=height))
        return face_render

    def display_all_faces(self):
        """
        Due to changes I'm not sure this works well. On my computer I have some issues with cv2, so they do not always display properly.

        :return: Displays all faces.
        """
        face_show = []
        face = [item[0:25][0] for item in list(self.face_type.values())]
        name = list(self.face_type.keys())
        for i in range(0, 25):
            face_show.append(np.array(face[i].face_render()))
            cv2.imshow(name[i], face_show[i])

    def create_face_gif(self):
        """
        :return: Creates and saves GIFs of all the faces in the current directory. The GIF are names after the faces that are displayed.
        """
        face = [item[0:25][0] for item in list(self.face_type.values())]
        name = list(self.face_type.keys())
        for i in range(1, 25):
            j = 0
            images = []
            for frames in np.linspace(0, 1, 33):
                temp_face_first_half = NeutralFace().interpolateface(NeutralFace(), frames)
                images.append(temp_face_first_half.face_render(width=960, height=540))
            for frames in np.linspace(0, 1, 11):
                temp_face_first_half = NeutralFace().interpolateface(face[i], frames)
                images.append(temp_face_first_half.face_render(width=960, height=540))
            for frames in np.linspace(0, 1, 33):
                temp_face_second_half = face[i].interpolateface(face[i], frames)
                images.append(temp_face_second_half.face_render(width=960, height=540))
            images[0].save('{}.gif'.format(name[i]), save_all=True, append_images=images[1:], duration=10)
            print('{} Face GIF completed. {}/24 completed.'.format(name[i], i))
