import cv2

from face_manager import FaceManager


fm = FaceManager(width=600, height=480)

while True:

    if cv2.waitKey(16) == 'a':
        fm.show_expression("happy", duration=4)

    face = fm.get_next_frame(delta=16, event=5)
    cv2.imshow("Face", face)
