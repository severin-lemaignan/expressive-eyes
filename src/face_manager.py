from expressive_eyes import *

key_event={
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

delta = 6000 # 6 s blinking time
Next_Face = NeutralFace()
int_speed = 70
blink_pos = BlinkMed()

for alpha in np.arange(0, 1, 0.1):  # On startup
    interpolation(BlinkMed(), NeutralFace(), alpha)
    cv2.waitKey(int_speed+20)

cv2.waitKey(4000)

while True:
    Prior_Face = Next_Face

    for alpha in np.arange(0, 1, 0.1):  # Blink down
        interpolation(Next_Face, blink_pos, alpha)
        cv2.waitKey(int_speed)

    for alpha in np.arange(0, 1, 0.1):  # Blink up
        interpolation(blink_pos, Next_Face, alpha)
        cv2.waitKey(int_speed)

    key = cv2.waitKey(delta)

    if key in range(97,122):  # a to y - all cv2.waitkey codes taken from http://www.asciitable.com/
        Next_Face, int_speed, blink_pos, delta = get_next_frame(Prior_Face, 0.1, key_event[key])
        cv2.waitKey(5000)
    elif key == 27:  # ESC
        cv2.destroyAllWindows()
        exit(0)

class FaceManager:

    def __init__(self):

        self.time = 0 # in ms

        self.time_last_blink = 0
        self.is_blinking = False

        self.next_expression = None
        self.next_expression_duration = 0
        self.time_started_expression = 0
        self.is_showing_expression = False

    def get_next_frame(self, delta):

        self.time += delta

        if self.time - self.time_last_blink > 6000:
            self.time_last_blink = self.time
            self.is_blinking = True

        if self.is_blinking:
            blinking_time = self.time - self.time_last_blink
            interpolateface(...)
            ...

        if self.next_expression is not None and not self.is_showing_expression:
            self.time_started_expression = self.time
            self.is_showing_expression = True

        if self.is_showing_expression:
            ...


        
    def show_expression(type, duration):
        self.next_expression = type
        self.next_expression_duration = duration

