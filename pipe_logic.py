class PipeGenerator:
    # TODO: drawing the rectangle begins at the top left corner,
    # not the center as previously assumed. below code needs to be
    # modified to reflect this
    def __init__(self, 
                 width, 
                 length,
                 speed, 
                 starting_x, 
                 interval,
                 screen_height):

        self.width = width
        self.length = length
        self.speed = speed
        self.starting_x = starting_x
        self.interval = interval
        self.screen_height = screen_height

        self.pipes = []
    def generate_pipe(self, length=None, reverse=False):
        new_pipe = None
        length_val = self.length if length == None else length
        y_val = 0 if reverse is False else self.screen_height - length_val
        new_pipe = Pipe(speed=self.speed, 
                        width=self.width, 
                        length=length_val, 
                        x=self.starting_x, 
                        y=y_val)
        self.pipes.append(new_pipe)
    def clean_pipes(self):
        clean_pipes = []
        for pipe in self.pipes:
            if pipe.x > -1*self.width:
                clean_pipes.append(pipe)
        self.pipes = clean_pipes
class Pipe:
    def __init__(self, 
                 speed, 
                 width, 
                 length, 
                 x,
                 y
                 ):
        self.speed = speed
        self.width = width
        self.length = length
        self.x = x
        self.y = y
    def step(self):
        self.x -= self.speed


