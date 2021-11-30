from face_manager import *
import cv2
import time
import expressions as exp
import numpy as np
import procedural_face as pf
from enum import IntEnum

# the instance of the ProceduralFaceGenerator class is taken so that the blinking can be done.
pfg = pf.ProceduralFaceGenerator()

# neutral_eyes is the instance of ProceduralFace object. It needed to be rescaled to make the transition from neutral face to an expression smoother. 
neutral_eyes = pf.ProceduralFace()
neutral_eyes.eyes[0].scale_x = 0.8
neutral_eyes.eyes[1].scale_x = 0.8
neutral_eyes.eyes[0].scale_y = 0.8
neutral_eyes.eyes[1].scale_y = 0.8

fm = FaceManager()

elapsed_time = 0
elapsed_time_2 = 0
begin_time = time.time()

# class of the emotions, this enumarator is used to specify the conditions inside of the below function.
class emotions(IntEnum):
    NEUTRAL = 0 
    HAPPY = 1
    ANGRY = 2
    SAD = 3
    SURPRISED = 4
    FEAR = 5
    DISGUST = 6

# the code starts with neutral face
current_emotion = emotions.NEUTRAL

def run_interactive_eyes(action_units, right_x, right_y, left_x, left_y):

    global elapsed_time_2
    global elapsed_time
    global begin_time
    global current_emotion
    global fm

    # if there is no expression shown by the user, then the code reflects neutral eyes that track the eyes of the user and imitate it (this is done by using cv2.imshow function of the opencv). Also, they blink every 5 seconds (this can be changed).
    if current_emotion == emotions.NEUTRAL:

        # X (going right is +, going left is -) AND Y (going down is +, going up is -)
        # # left eye, x and y coordinates of the center, respectively (x = [5], y = [6])
        neutral_eyes.params[5] = - 3*left_x
        neutral_eyes.params[6] = 6*left_y

        # # right eye, x and y coordinates of the center, respectively (x = [24], y = [25])
        neutral_eyes.params[24] = - 3*right_x
        neutral_eyes.params[25] = 6*right_y


        im = neutral_eyes.render().convert('RGB')
        np_im = np.array(im)
        k = cv2.waitKey(1) & 0xFF
        cv2.imshow("all EYEZ on you", np_im)
        print(elapsed_time_2)   

        elapsed_time_2 = time.time() - begin_time

        # blinking time is set as seconds.
        if elapsed_time_2 >= 5:
            begin_time = time.time()
            pfg._blink()
        
        # the below set of code checks the intensity values of the action units and if there is a matched one, it runs the function called 'set_next_expression' and this function creates a face_list with a specific number of frames (length). Afterwards, the below code runs. 
        if action_units[15].intensity > 2:
            current_emotion = emotions.HAPPY
            fm.set_next_expression(exp.Happiness(), 2)

        if action_units[10].intensity > 3.5 and action_units[4].intensity > 2.5 and action_units[14].intensity <= 2.25:
            current_emotion = emotions.SURPRISED
            fm.set_next_expression(exp.Surprise(), 2)
    
        if action_units[4].intensity > 2 and action_units[12].intensity > 2:
            current_emotion = emotions.SAD
            fm.set_next_expression(exp.Sadness(), 2)

        if action_units[14].intensity > 3:
            current_emotion = emotions.ANGRY
            fm.set_next_expression(exp.Anger(), 2)

        if action_units[11].intensity > 1 and action_units[14].intensity <= 3:
            current_emotion = emotions.DISGUST
            fm.set_next_expression(exp.Disgust(), 2)

        # This expression(fear) is causing a conflict with surprised face so 'fear' won't be included in the experiment design.
        # # if action_units[4].intensity > 2.75 and action_units[14].intensity > 2.25 and action_units[10].intensity > 2.5:
        # #     current_emotion = emotions.FEAR
        # #     fm.set_next_expression(exp.Fear(), 3)

        # Index and related AU number for the code above
        # 0 - 28
        # 1 - 45
        # 2 - 26
        # 3 - 25
        # 4 - 1
        # 5 - 5
        # 6 - 20
        # 7 - 6
        # 8 - 23
        # 9 - 7
        # 10 - 2
        # 11 - 9
        # 12 - 17
        # 13 - 10
        # 14 - 4
        # 15 - 12
        # 16 - 14
        # 17 - 15


    # Inside of this condition where an expressions is showed, the function called 'get_next_frame' decides which frame will be shown according to the elapsed time, and the animation is reflected by using the opencv cv2.imshow function again. If the expression is finished, then the system waits 2 seconds (this can be changed as well) and comes back to neutral face again.    
    if current_emotion != emotions.NEUTRAL:
        print(elapsed_time)
        last_time = time.time()*1000.0
        face = fm.get_next_frame(elapsed_time)
        im = face.render().convert('RGB')
        np_im = np.array(im)
        k = cv2.waitKey(1) & 0xFF
        cv2.imshow("all EYEZ on you", np_im)
        elapsed_time = time.time()*1000.0 - last_time

        if fm.next_expression == None:
            fm = FaceManager()
            current_emotion = emotions.NEUTRAL    
            time.sleep(2)
            begin_time = time.time()
        
            

# ELAPSED TIME = TIME PASSED FOR EACH LOOP
