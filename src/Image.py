#!/usr/bin/env python
import imageio
import PIL
from PIL import Image
from pathlib import Path
import pycozmo
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

CENTER_X = (0, 0., 1.)
CENTER_Y = (1, 0., 360.)
...

DEFAULT_EYE = {
        CENTER_X: 0,
        SCALE_X: 1.0,
        ...
        }

class Face:
    def __init__(self, eye_parameters):

        self.eye = DEFAULT_EYE
        for k, v in eye_parameters.items():
            self.eye[k] = v


        self.center_x = 0; self.center_y = 0
        self.scale_x = 1.0; self.scale_y = 1.0
        self.angle = 0.0
        self.lower_inner_radius_x = 0.5; self.lower_inner_radius_y = 0.5
        self.lower_outer_radius_x = 0.5; self.lower_outer_radius_y = 0.5
        self.upper_inner_radius_x = 0.5; self.upper_inner_radius_y = 0.5
        self.upper_outer_radius_x = 0.5; self.upper_outer_radius_y = 0.5
        self.upper_lid_y = 0.0; self.upper_lid_angle = 0.0; self.upper_lid_bend = 0.0
        self.lower_lid_y = 0.0; self.lower_lid_angle = 0.0; self.lower_lid_bend = 0.0

        self.left = [self.center_x, self.center_y, self.scale_x, self.scale_y, self.angle,
                     self.lower_inner_radius_x, self.lower_inner_radius_y,
                     self.lower_outer_radius_x, self.lower_outer_radius_y,
                     self.upper_inner_radius_x, self.upper_inner_radius_y,
                     self.upper_outer_radius_x, self.upper_outer_radius_y,
                     self.upper_lid_y, -self.upper_lid_angle, self.upper_lid_bend,
                     self.lower_lid_y, self.lower_lid_angle, self.lower_lid_bend]

        self.right = [self.center_x, self.center_y, self.scale_x, self.scale_y, self.angle,
                      self.lower_inner_radius_x, self.lower_inner_radius_y,
                      self.lower_outer_radius_x, self.lower_outer_radius_y,
                      self.upper_inner_radius_x, self.upper_inner_radius_y,
                      self.upper_outer_radius_x, self.upper_outer_radius_y,
                      self.upper_lid_y, self.upper_lid_angle, self.upper_lid_bend,
                      self.lower_lid_y, self.lower_lid_angle, self.lower_lid_bend]

        # self.left = [0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # self.right = [0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def interpolate(face, alpha):

        interpolated_face = Face()

        for k in self.eye:
        

            x = [0, 1]
            y = [ self.eye[k], face[k] ]
            f = interpolate.interp1d(x, y)

            interpolated_face[k] = f(alpha)

        return interpolated_face
   

    def render(self):
        face = pycozmo.procedural_face.ProceduralFace(left_eye=self.left, right_eye=self.right)
        return face.render().convert('RGB')


class AngryFace(Face):
    def __init__(self, upper_lid_y, upper_lid_angle):
        super().__init__({
                            UPPER_LID_Y: upper_lid_y, 
                            UPPER_LID_ANGLE: upper_lid_angle
                        })

        # pre-define parameters for an angry face
        self.upper_lid_y = upper_lid_y
        self.upper_lid_angle = upper_lid_angle

        self.left = [0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -30.0, 0.0, 0.0, 0.0, 0.0]
        self.right = [0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 30.0, 0.0, 0.0, 0.0, 0.0]


class SadFace(Face):
    def __init__(self):
        super().__init__()
        self.left = [0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 20.0, 0.0, 0.0, 0.0, 0.0]
        self.right = [0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, -20.0, 0.0, 0.0, 0.0, 0.0]


face2 = Face()
#  face3 = SadFace()
face1 = AngryFace(0.5, 30.0)

x=np.arange(0.5, 30)
y=x**3
f = interpolate.interp1d(x, y)
xnew=np.arange(0.5, 29.6, 0.1)
ynew=f(xnew)

plt.plot(x, y, 'o', xnew, ynew, '-')
plt.show()


def main():
    im1 = face1.render()
    end1 = pycozmo.procedural_face.ProceduralFace()
    # im1 = end1.render()
    im1.show()


    happy_face = HappyFace()
    sad_face = SadFace()

    for i in range(20):
        inbetween = happy_face.interpolate(sad_face, 1./i)
        im = inbetween.render()
        im.show()


    #interpolating_face = happy_face.interpolate(sad_face)

    #face = interpolating_face(alpha)


# frames = [face2, face1]
# frames[0].save('out.gif', save_all=True)


if __name__ == '__main__':
    main()
