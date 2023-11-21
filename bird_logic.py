import random
class Bird:

    def __init__(self, x=0, y=0, size=50, screen_height=None, neural_net=None):
        self.x = x
        self.y = y
        self.color = (random.randint(0,255), 
                      random.randint(0,255),
                      random.randint(0,255),
                      )
        self.size = size
        self.accel = -5
        self.base_accel = -10
        self.step_size = 2
        self.screen_height = screen_height
        self.alive = True
        self.survival_time = 0
        self.neural_net = neural_net

    def step(self):
        self.y -= self.accel*self.step_size
        self.survival_time += 1
        if self.accel > self.base_accel:
            self.accel -= 2
    def jump(self, p1_y=None, p2_y=None, p_x=None):
        if self.neural_net is not None:
            #if self.survival_time % 5 == 0:
            if True:
                inputs = [self.accel, p1_y, p2_y, p_x, self.y]
                #print(f"accel: {self.accel} p1_y: {p1_y}, p2_y: {p2_y}  p_x: {p_x} self ypos: {self.y}")
                jump_prob = self.neural_net.forward(inputs)
                # print(f"jump probability: {jump_prob}")
                if jump_prob > 0.5:
                    self.accel = 12
        else:
            self.accel = 20
    def check_collision(self, pipe):
        if pipe.y <= self.y <= pipe.y + pipe.length:
            if pipe.x <= self.x + self.size <= pipe.x + pipe.width:
                #print("bird died: collided with pipe")
                self.y = 0
                self.alive = False
                return True
        if (self.y + self.size > self.screen_height or
            self.y < 0):
            #print("bird died: too high or too low")
            #print(f'bird height: {self.y}; max height: {self.screen_height}')
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









