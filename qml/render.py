#
# PyOtherSide: Asynchronous Python 3 Bindings for Qt 5
# Copyright (c) 2011, 2013, Thomas Perl <m@thp.io>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import pyotherside
import os

import time

from PIL import Image

class FaceManager():
    def __init__(self):
        self.last_render = time.time()

    def get_elapsed_time(self):
        now = time.time()
        elapsed_time = self.last_render - now
        self.last_render = now

        return elapsed_time

def render(image_id, requested_size):
    
    elapsed_time = facemanager.get_elapsed_time()

    img_name, unique_token = image_id.split("?")
    print('image_id: "{img_name}" (elapsed: {elapsed_time}s, token: {unique_token}), size: {requested_size}'.format(**locals()))

    # width and height will be -1 if not set in QML
    if requested_size == (-1, -1):
        requested_size = (128, 64)


    filename = os.path.join(os.path.dirname(__file__), image_id)
    img = Image.open(filename)

    img.thumbnail(requested_size, Image.ANTIALIAS)

    #b, g, r, a = img.split()
    #img = Image.merge("RGBA", (r, g, b, a))
    return bytearray(img.tobytes()), img.size, pyotherside.format_argb32

facemanager = FaceManager()

pyotherside.set_image_provider(render)
