import expressions as exp
import procedural_face as pf

class FaceManager:

    def __init__(self):
        self.current_expression = exp.Neutral()
        self.next_expression = None

        self.ideal_FPS = 200

        self.current_frame_idx = 0

        self.ideal_time_between_frames = float(1000.0 / self.ideal_FPS ) # miliseconds (5ms)



    # create a face_list array (the number of frames is calculated according to the duration time)
    # this function takes two variables: expression and duration time. While the expression is a procedural face object, duration needs to be given as seconds.
    def set_next_expression(self, expression, duration):
        number_of_frames = duration * self.ideal_FPS
        self.next_expression = expression
        self.face_list = list(pf.interpolate(self.current_expression, self.next_expression , number_of_frames))
        self.current_frame_idx = 0

    # according to the time passed per loop, some of the frames are skipped to ensure that the expression will finish in time
    def get_next_frame(self, elapsed_time):


        if 0 < elapsed_time <= 5:
            self.current_frame_idx += 3

        elif 5 < elapsed_time <= 10 :
            self.current_frame_idx += 6

        elif 10 < elapsed_time <= 15 :
            self.current_frame_idx += 9

        elif 15 < elapsed_time <= 20:
            self.current_frame_idx += 12
        
        elif 20 < elapsed_time <= 25:
            self.current_frame_idx += 15
        
        elif 25 < elapsed_time <= 30:
            self.current_frame_idx += 18

        elif 30 < elapsed_time <= 35:
            self.current_frame_idx += 21

        elif 35 < elapsed_time:
            self.current_frame_idx += 24

        # if all the frames are shown, then stop the interpolation
        if self.current_frame_idx >= (len(self.face_list)):
            self.current_expression = None
            self.next_expression = None
            self.current_frame_idx = 0
            return self.current_expression

        return self.face_list[self.current_frame_idx]

        
