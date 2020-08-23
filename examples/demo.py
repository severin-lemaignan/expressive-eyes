from face_manager import FaceManager
import cv2
import time

fm = FaceManager(1920, 1080)
key_event = {
    97: "Neutral",
    98: "Happy",
    99: "Amazed",
    100: "Excited",
    101: "Angry",
    102: "Surprised",
    103: "Fear",
    104: "Despair",
    105: "Disappointed",
    106: "Embarrassed",
    107: "Horrified",
    108: "Annoyed",
    109: "Furious",
    110: "Disgust",
    111: "Pleading",
    112: "Guilty",
    113: "Skeptical",
    114: "Suspicious",
    115: "Confused",
    116: "Sad",
    117: "Vulnerable",
    118: "Rejected",
    119: "Bored",
    120: "Tired",
    121: "Asleep"
}
elapsed_time = 0

while True:
    begin_time = time.time()
    face = fm.run_expressive_eyes(face_str="Angry", elapsed_time=elapsed_time)
    elapsed_time = time.time() - begin_time
    cv2.waitKey(int(1000*elapsed_time))
    cv2.imshow("Face", face)
