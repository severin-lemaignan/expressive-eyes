
import cv2

import time

from expressive_eyes import ExpressiveEyes


eyes = ExpressiveEyes()


delta = 0.016 # 16 ms

while True:

    l_eye, r_eye = eyes.get_next_frame(delta)

    cv2.imshow("Left eye", l_eye)

    key = cv2.waitKey(delta) # sleeps 16ms

    if key == 32: # space
        eyes.set_target("happy")
        
    


