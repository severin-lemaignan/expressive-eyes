#!/usr/bin/env python
import imageio
import PIL
from PIL import Image
from pathlib import Path

import pycozmo


def main():
    # Render a 128x64 procedural face with default parameters.
    start = pycozmo.procedural_face.ProceduralFace()
    end1 = pycozmo.procedural_face.ProceduralFace(left_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                            0.5, 0.5, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0],
                                                  right_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                             0.5, 0.5, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0])
    end2 = pycozmo.procedural_face.ProceduralFace(left_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                            0.5, 0.5, 0.2, 0.0, .2, 0.0, 0.0, 0.0],
                                                  right_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                             0.5, 0.5, 0.2, 0.0, .2, 0.0, 0.0, 0.0])
    end3 = pycozmo.procedural_face.ProceduralFace(left_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                            0.5, 0.5, 0.3, 0.0, .3, 0.0, 0.0, 0.0],
                                                  right_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                             0.5, 0.5, 0.3, 0.0, .3, 0.0, 0.0, 0.0])
    end4 = pycozmo.procedural_face.ProceduralFace(left_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                            0.5, 0.5, 0.4, 0.0, .4, 0.0, 0.0, 0.0],
                                                  right_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                             0.5, 0.5, 0.4, 0.0, .4, 0.0, 0.0, 0.0])
    end = pycozmo.procedural_face.ProceduralFace(left_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                           0.5, 0.5, 0.5, 0.0, .5, 0.0, 0.0, 0.0],
                                                 right_eye=[0, 0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                            0.5, 0.5, 0.5, 0.0, .5, 0.0, 0.0, 0.0])
    
    frames = []

    frames.append(start.render().convert('RGB'))
    frames.append(end1.render().convert('RGB'))
    frames.append(end2.render().convert('RGB'))
    frames.append(end3.render().convert('RGB'))
    frames.append(end4.render().convert('RGB'))
    frames.append(end.render().convert('RGB'))

    frames[0].save('out.gif', save_all=True, append_images=frames[1:])


if __name__ == '__main__':
    main()

#  center_x: int = 0, center_y: int = 0,
#  scale_x: float = 1.0, scale_y: float = 1.0,
#  angle: float = 0.0,
#  lower_inner_radius_x: float = 0.5, lower_inner_radius_y: float = 0.5,
#  lower_outer_radius_x: float = 0.5, lower_outer_radius_y: float = 0.5,
#  upper_inner_radius_x: float = 0.5, upper_inner_radius_y: float = 0.5,
#  upper_outer_radius_x: float = 0.5, upper_outer_radius_y: float = 0.5,
#  upper_lid_y: float = 0.0, upper_lid_angle: float = 0.0,
#  upper_lid_bend: float = 0.0, lower_lid_y: float = 0.0,
#  lower_lid_angle: float = 0.0, lower_lid_bend: float = 0.0):


