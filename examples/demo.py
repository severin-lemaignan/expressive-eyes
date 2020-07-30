import cv2

from expressive_eyes.face_manager import *


fm = FaceManager(width=600, height=480)
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

event_key = 0
while True:
    key = cv2.waitKey(100)

    if key == 122: # z
        fm.show_expression("Happy", duration=400)
        print("Happy")

    if key in range(97, 122):  # a to y
        event_key = key_event[key]
    elif key == 27:  # ESC
        cv2.destroyAllWindows()
        exit(0)

    face = fm.get_next_frame(event=event_key, duration=500)

    for i in face:
        cv2.imshow("Face", i)
