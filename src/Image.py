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
    im1 = start.render()
    im1.show()
    im2 = end1.render()
    im2.show()
    im3 = end2.render()
    im3.show()
    im4 = end3.render()
    im4.show()
    im5 = end4.render()
    im5.show()
    im = end.render()
    im.show()
    im = im.convert("RGB")
    im1 = im1.convert("RGB")
    im2 = im2.convert("RGB")
    im3 = im3.convert("RGB")
    im4 = im4.convert("RGB")
    im5 = im5.convert("RGB")
    im15 = PIL.Image.blend(im2, im3, 0.5)
    im05 = PIL.Image.blend(im1, im2, 0.5)
    im25 = PIL.Image.blend(im3, im4, 0.5)
    im35 = PIL.Image.blend(im4, im5, 0.5)
    im45 = PIL.Image.blend(im5, im, 0.5)
    im05.show()
    im15.show()
    im25.show()
    im35.show()
    im45.show()

    print(type(im))


if __name__ == '__main__':
    main()

image_path = Path('/home/catherine/Downloads/pycozmo-master/source_images/Blinking')
images = list(image_path.glob('*.png'))

image_list = []

for file_name in images:
    image_list.append(imageio.imread(file_name))

imageio.mimwrite('animated_from_images.gif', image_list, fps=1)
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


