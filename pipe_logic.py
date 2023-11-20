class PipeGenerator:
    # TODO: drawing the rectangle begins at the top left corner,
    # not the center as previously assumed. below code needs to be
    # modified to reflect this
    def __init__(self, 
                 pipe_width, 
                 pipe_speed, 
                 x_start, 
                 pipe_interval,
                 pipe_height,
                 screen_height):
        self.pipe_width = pipe_width
        self.pipe_speed = pipe_speed
        self.pipe_height = pipe_height
        self.x_start = x_start
        self.pipe_interval = pipe_interval
        self.pipes = []
        self.screen_height = screen_height
    def generate_pipe(self, 
                      pipe_top, 
                      pipe_bottom,
                      reverse=False,
                      pipe_size_multiplier=100):
        new_pipe = None
        if reverse is False:
            new_pipe = Pipe(self.pipe_speed, 
                        self.pipe_width, 
                        pipe_top, 
                        pipe_bottom,
                        self.x_start)
        else:
            new_pipe = Pipe(self.pipe_speed, 
                        self.pipe_width, 
                        self.screen_height - pipe_bottom, 
                        self.screen_height,
                        self.x_start,
                        y=self.screen_height-pipe_bottom)


        self.pipes.append(new_pipe)
    def clean_pipes(self):
        clean_pipes = []
        for pipe in self.pipes:
            if pipe.x > -1*self.pipe_width:
                clean_pipes.append(pipe)
        self.pipes = clean_pipes
class Pipe:
    def __init__(self, 
                 horizontal_speed, 
                 width, 
                 top, 
                 bottom, 
                 x_start,
                 y=0
                 ):
        self.horizontal_speed = horizontal_speed
        self.width = width
        self.top = top
        self.bottom = bottom
        self.x = x_start
        self.y = y
        #print(top, bottom, self.y)
        self.length = abs(top-bottom)*10
    def step(self):
        self.x -= self.horizontal_speed


