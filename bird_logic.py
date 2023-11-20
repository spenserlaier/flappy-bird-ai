class Bird:
    def __init__(self, x=0, y=0, size=50, screen_height=400):
        self.x = x
        self.y = y
        self.size = size
        self.accel = -5
        self.base_accel = -10
        self.step_size = 2
        self.screen_height = screen_height
        self.alive = True

    def step(self):
        self.y -= self.accel*self.step_size
        if self.accel > self.base_accel:
            self.accel -= 2
    def jump(self):
        self.accel = 20
    def check_collision(self, pipe):
        if pipe.y <= self.y <= pipe.y + pipe.length:
            if pipe.x <= self.x + self.size <= pipe.x + pipe.width:
                self.y = 0
                self.alive = False
                return True
        if (self.y + self.size > self.screen_height or
            self.y < 0):
            self.y = 0
            self.alive = False
            return True
        return False


    def get_pipe_dist(self, pipe, reverse=False):
        x_dist = abs(pipe.x - (self.x + self.size))
        y_dist = None
        if reverse is False:
            y_dist = abs((pipe.y + pipe.length) - (self.y))
        else:
            y_dist = abs(pipe.y - self.y)
        return (x_dist, y_dist)









