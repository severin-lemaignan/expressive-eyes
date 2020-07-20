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
