#!/usr/bin/env python
from Image import *
import imageio
import PIL
from PIL import Image
from pathlib import Path
import pycozmo
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time

# All cv2.waitkey codes taken from http://www.asciitable.com/

# Perplexed/Skeptical
test_face = pycozmo.procedural_face.ProceduralFace(
        left_eye=[0, 0,
                  1.0, 1.0,
                  0.0,
                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                  0.0, 30.0, 0.0, 0.0, 0.0, 0.0],
        right_eye=[0, 0,
                   1.0, 1.0,
                   0.0,
                   0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                   0.0, -30.0, 0.0, 0.0, 0.0, 0.0])
def main():
    test_face1 = SkepticalFace()
    im1 = test_face.render()
    im1.show()
    face2 = NeutralFace()
    face1 = SadFace()
    # for alpha in np.arange(0, 1, 0.1):
    #     face3 = face2.interpolateface(face1, alpha)
    #     #face3 = test_face1
    #     dst = cv2.medianBlur(np.array(face3.render()),5)
    #     large = cv2.resize(dst, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
    #     cv2.imshow("image", cv2.blur(large,(15,15)))
    #     cv2.waitKey(10)


if __name__ == '__main__':
    main()

# CENTER_X = (0, -50, 50); CENTER_Y = (0, -50, 50)
# SCALE_X = (1.0, 1.0, 1.0); SCALE_Y = (1.0, 1.0, 1.0); ANGLE = (0.0, 0.0, 360.0)
# LOWER_INNER_RADIUS_X = (0.5, 0.0, 1.0); LOWER_INNER_RADIUS_Y = (0.5, 0.0, 0.6)
# LOWER_OUTER_RADIUS_X = (0.5, 0.0, 1.0); LOWER_OUTER_RADIUS_Y = (0.5, 0.0, 5.0)
# UPPER_INNER_RADIUS_X = (0.5, 0.0, 1.0); UPPER_INNER_RADIUS_Y = (0.5, 0.0, 0.6)
# UPPER_OUTER_RADIUS_X = (0.5, 0.0, 1.0); UPPER_OUTER_RADIUS_Y = (0.5, 0.0, 5.0)
# UPPER_LID_Y = (0.0, 0.0, 1.0); UPPER_LID_ANGLE = (0.0, -60.0, 60.0); UPPER_LID_BEND = (0.0, 0.0, 1.0)
# LOWER_LID_Y = (0.0, 0.0, 1.0); LOWER_LID_ANGLE = (0.0, -60.0, 60.0); LOWER_LID_BEND = (0.0, 0.0, 1.0)


# class NeutralFace(Face):
# #  Six basic expressions by Ekman
# class AngryFace(Face):
# class SadFace(Face):
# class HappyFace(Face):
# class SurprisedFace(Face):
# class DisgustFace(Face):
# class FearFace(Face):
# # Sub-faces of sadness
# # Pleading is directional related (i.e. looking up, head down, is normally associated with pleading)
# class PleadingFace(Face):
# class VulnerableFace(Face):
# class DespairFace(Face):
# class GuiltyFace(Face):
# class DisappointedFace(Face):
# class EmbarrassedFace(Face):
# # Sub-face of disgust.
# class HorrifiedFace(Face):
# # Sub-faces of anger.
# # Skeptical is similar to perplexed.
# class SkepticalFace(Face):
# class AnnoyedFace(Face):
# # Also known as enraged
# class FuriousFace(Face):
# class BitterFace(Face):
# class BetrayedFace(Face):
# class SuspiciousFace(Face):
# # Sub-faces of fear.
# class NervousFace(Face):
# # Taken from "withdrawn"
# class RejectedFace(Face):
# # Sub-faces of "bad" emotions
# class BoredFace(Face):
# class TiredFace(Face):
# class AsleepFace(Face):
# # Sub-faces of surprise.
# class ConfusedFace(Face):
# class PerplexedFace(Face):
# class AmazedFace(Face):
# class ExcitedFace(Face):

        # if event == 0: # Neutral face on startup - med arousal med valence
        #     self.facemanager.next_target(NeutralFace(), intensity = 9, transition_duration=4)
        #
        # # Six "basic" emotions
        # elif event == 1: # Angry - high arousal low valence
        #     self.facemanager.next_target(AngryFace(), intensity = 5, transition_duration=4)
        # elif event == 2: # Sad - low arousal low valence
        #     self.facemanager.next_target(SadFace(), intensity = 5, transition_duration=4)
        # elif event == 3: # Happy - high arousal high valence
        #     self.facemanager.next_target(HappyFace(), intensity = 5, transition_duration=4)
        # elif event == 4: # Surprised - high arousal low valence
        #     self.facemanager.next_target(SurprisedFace(), intensity = 5, transition_duration=4)
        # elif event == 5: # Disgust - med arousal low valence
        #     self.facemanager.next_target(DisgustFace(), intensity = 5, transition_duration=4)
        # elif event == 6: # Fear - high arousal low valence
        #     self.facemanager.next_target(FearFace(), intensity = 5, transition_duration=4)
        #
        # # Sadness based emotions
        # elif event == 7: # Pleading - med arousal low valence
        #     self.facemanager.next_target(PleadingFace(), intensity = 5, transition_duration=4)
        # elif event == 8: # Vulnerable - low arousal low valence
        #     self.facemanager.next_target(VulnerableFace(), intensity = 5, transition_duration=4)
        # elif event == 9: # Despair - high arousal low valence
        #     self.facemanager.next_target(DespairFace(), intensity = 5, transition_duration=4)
        # elif event == 10: # Guilty - med arousal low valence
        #     self.facemanager.next_target(GuiltyFace(), intensity = 5, transition_duration=4)
        # elif event == 11: # Disappointed - high arousal low valence
        #     self.facemanager.next_target(DisappointedFace(), intensity = 5, transition_duration=4)
        # elif event == 12: # Embarrassed - high arousal low valence
        #     self.facemanager.next_target(EmbarrassedFace(), intensity = 5, transition_duration=4)
        #
        # # Disgust based emotion
        # elif event == 13: # Horrified - high arousal low valence
        #     self.facemanager.next_target(HorrifiedFace(), intensity = 5, transition_duration=4)
        #
        # # Anger based emotions
        # elif event == 14: # Skeptical - med arousal low valence
        #     self.facemanager.next_target(SkepticalFace(), intensity = 5, transition_duration=4)
        # elif event == 15: # Annoyed - high arousal low valence
        #     self.facemanager.next_target(AnnoyedFace(), intensity = 5, transition_duration=4)
        # elif event == 16: # Furious - high arousal low valence
        #     self.facemanager.next_target(FuriousFace(), intensity = 5, transition_duration=4)
        # elif event == 17: # Bitter - med arousal low valence
        #     self.facemanager.next_target(BitterFace(), intensity = 5, transition_duration=4)
        # elif event == 18: # Betrayed - high arousal low valence
        #     self.facemanager.next_target(BetrayedFace(), intensity = 5, transition_duration=4)
        # elif event == 19: # Suspicious - med arousal low valence
        #     self.facemanager.next_target(SuspiciousFace(), intensity = 5, transition_duration=4)
        #
        # # Fear based emotions
        # elif event == 20: # Nervous - med arousal low valence
        #     self.facemanager.next_target(NervousFace(), intensity = 5, transition_duration=4)
        # elif event == 21: # Rejected - low arousal low valence
        #     self.facemanager.next_target(RejectedFace(), intensity = 5, transition_duration=4)
        #
        # # "Bad" emotions
        # elif event == 22: # Bored - low arousal low valence
        #     self.facemanager.next_target(BoredFace(), intensity = 5, transition_duration=4)
        # elif event == 23: # Tired - low arousal low valence
        #     self.facemanager.next_target(TiredFace(), intensity = 5, transition_duration=4)
        # elif event == 24: # Asleep - low arousal low valence
        #     self.facemanager.next_target(AsleepFace(), intensity = 5, transition_duration=4)
        #
        # # Surprise based emotions
        # elif event == 25: # Confused - med arousal low valence
        #     self.facemanager.next_target(ConfusedFace(), intensity = 5, transition_duration=4)
        # elif event == 26: # Perplexed - med arousal low valence
        #     self.facemanager.next_target(PerplexedFace(), intensity = 5, transition_duration=4)
        # elif event == 27: # Amazed - high arousal high valence
        #     self.facemanager.next_target(AmazedFace(), intensity = 5, transition_duration=4)
        # elif event == 28: # Excited - high arousal high valence
        #     self.facemanager.next_target(ExcitedFace(), intensity = 5, transition_duration=4)

    # if key == 97: # a
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 1)
    # elif key == 98: # b
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 2)
    # elif key == 99: # c
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 3)
    # elif key == 100: # d
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 4)
    # elif key == 101: # e
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 5)
    # elif key == 102: # f
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 6)
    # elif key == 103: # g
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 7)
    # elif key == 104: # h
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 8)
    # elif key == 105: # i
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 9)
    # elif key == 106: # j
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 10)
    # elif key == 107: # k
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 11)
    # elif key == 108: # l
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 12)
    # elif key == 109: # m
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 13)
    # elif key == 110: # n
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 14)
    # elif key == 111: # o
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 15)
    # elif key == 112: # p
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 16)
    # elif key == 113: # q
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 17)
    # elif key == 114: # r
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 18)
    # elif key == 115: # s
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 19)
    # elif key == 116: # t
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 20)
    # elif key == 117: # u
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 21)
    # elif key == 118: # v
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 22)
    # elif key == 119: # w
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 23)
    # elif key == 120: # x
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 24)
    # elif key == 121: # y
    #     Next_Face, int_speed, blink_height = eyes.get_next_frame(Prior_Face, int_speed, 0)
