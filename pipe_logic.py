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
                 screen_height,
                 gap_size=40):

        self.width = width
        self.length = length
        self.speed = speed
        self.starting_x = starting_x
        self.interval = interval
        self.screen_height = screen_height
        self.gap_size = gap_size

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
        return new_pipe
    def generate_pipe_pair(self, gap_height):
        #the top pipe extends from the top of the screen down to the top left corner of the gap
        #the bottom pipe begins from the end of the top pipe + the gap height down to the bottom of the screen
        top_pipe_length = gap_height
        bottom_pipe_length =   self.screen_height - top_pipe_length - self.gap_size
        top_pipe = self.generate_pipe(top_pipe_length)
        bot_pipe = self.generate_pipe(bottom_pipe_length, reverse=True)
        print('generating pipe pair')
        #self.pipes.append(top_pipe)
        #self.pipes.append(bot_pipe)
        self.pipes.append((top_pipe, bot_pipe))



    def clean_pipes(self):
        clean_pipes = []
        for p1, p2 in self.pipes:
            if p1.x > -1*self.width:
                clean_pipes.append((p1, p2))
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


