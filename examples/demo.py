from expressive_eyes.face_manager import FaceManager
import cv2
import time

fm = FaceManager(192, 108)

elapsed_time = 0

while True:
    begin_time = time.time()
    face = fm.run_expressive_eyes(face_str="Neutral", elapsed_time=elapsed_time)
    elapsed_time = time.time() - begin_time
    # I am not sure about the following wait_time.
    wait_time = int(1000*elapsed_time/2)
    # This waitKey is needed to properly display the interpolated face
    cv2.waitKey(wait_time)
    # This is needed to display the face render
    cv2.imshow("Face", face)
