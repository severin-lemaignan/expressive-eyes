#! /bin/env python3

from expressive_eyes.face_manager import FaceManager
from expressive_eyes import expressions as exp
import cv2
import time

fm = FaceManager()

elapsed_time = 0

fm.set_next_expression(exp.get("Happy"), 1)

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

current_valence = 0
current_arousal = 0

while True:
    begin_time = time.time()
    face = fm.step(elapsed_time * 1000)

    key = cv2.waitKey(16)
    if key == 27:
        break
    elif key == ord("q"):
        fm.set_next_expression(exp.get("Neutral"), 1)
    elif key == ord("w"):
        fm.set_next_expression(exp.get("Anger"), 1)
    elif key == ord("e"):
        fm.set_next_expression(exp.get("Sadness"), 1)
    elif key == ord("r"):
        fm.set_next_expression(exp.get("Happy"), 1)
    elif key == ord("t"):
        fm.set_next_expression(exp.get("Surprise"), 1)
    elif key == ord("y"):
        fm.set_next_expression(exp.get("Disgust"), 1)
    elif key == ord("u"):
        fm.set_next_expression(exp.get("Fear"), 1)
    elif key == ord("i"):
        fm.set_next_expression(exp.get("Tired"), 1)
    elif key == ord("o"):
        fm.set_next_expression(exp.get("Excited"), 1)
    elif key == ord("p"):
        fm.set_next_expression(exp.get("Confused"), 1)
    elif key == 81:  # left
        current_valence = max(-1.0, current_valence - 0.1)
        print(f"Valence: {current_valence}, arousal: {current_arousal}")
        fm.set_next_expression(
            exp.get_valence_arousal(current_valence, current_arousal), 1
        )

    elif key == 83:  # right
        current_valence = min(1.0, current_valence + 0.1)
        print(f"Valence: {current_valence}, arousal: {current_arousal}")
        fm.set_next_expression(
            exp.get_valence_arousal(current_valence, current_arousal), 1
        )

    elif key == 82:  # up
        current_arousal = min(1.0, current_arousal + 0.1)
        print(f"Valence: {current_valence}, arousal: {current_arousal}")
        fm.set_next_expression(
            exp.get_valence_arousal(current_valence, current_arousal), 1
        )

    elif key == 84:  # down
        current_arousal = max(-1.0, current_arousal - 0.1)
        print(f"Valence: {current_valence}, arousal: {current_arousal}")
        fm.set_next_expression(
            exp.get_valence_arousal(current_valence, current_arousal), 1
        )

    cv2.imshow("window", face.render_to_cv())
    elapsed_time = time.time() - begin_time
