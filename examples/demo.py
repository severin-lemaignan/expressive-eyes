import cv2

from expressive_eyes.face_manager import *

fm = FaceManager(width=1980, height=1080)
key_event = {
    97: 1,
    98: 2,
    99: 3,
    100: 4,
    101: 5,
    102: 6,
    103: 7,
    104: 8,
    105: 9,
    106: 10,
    107: 11,
    108: 12,
    109: 13,
    110: 14,
    111: 15,
    112: 16,
    113: 17,
    114: 18,
    115: 19,
    116: 20,
    117: 21,
    118: 22,
    119: 23,
    120: 24,
    121: 0
}

# fm.display_all_faces()

while True:
    face = fm.get_next_frame(event=4, elapsed_time_since_last_call=1000)
    cv2.waitKey(10)
    cv2.imshow("Face", face)
