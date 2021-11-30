#!/usr/bin/env python
# subscriber for python

import rospy
from openface2_ros.msg import Faces
from face_manager import *
from run_eyes import *


def callback(faces):    

        # action units as list and x,y parameters for the eyes are instantly taken from the openface2_ros node's message called 'faces' 
        aus = faces.faces[0].action_units

        right_eye_x = faces.faces[0].right_gaze.position.x
        right_eye_y = faces.faces[0].right_gaze.position.y
        left_eye_x = faces.faces[0].left_gaze.position.x
        left_eye_y = faces.faces[0].left_gaze.position.y

        # the main function is called continuously 
        run_interactive_eyes(aus, right_eye_x, right_eye_y, left_eye_x, left_eye_y)

def listener():

    rospy.init_node('au_listener', anonymous=True)

    rospy.Subscriber('/openface2/faces', Faces, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
