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

delta = 16 # 16 ms
Next_Face = NeutralFace()
int_speed = 0.1

for alpha in np.arange(0, 1, int_speed):  # On startup
    interpolation(BlinkMed(), NeutralFace(), alpha)
    cv2.waitKey(100)

while True:
    Prior_Face = Next_Face
    key = cv2.waitKey(delta) # sleeps 16ms

    if key in range(97,122):  # a to y
        Next_Face, int_speed, blink_height = get_next_frame(Prior_Face, int_speed, key_event[key])
    elif key == 27:  # ESC
        cv2.destroyAllWindows()
        exit(0)


