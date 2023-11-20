class Bird:
    def __init__(self, x=0, y=0, size=50):
        self.x = x
        self.y = y
        self.size = size
        self.accel = -5
        self.base_accel = -5
        self.step_size = 2

    def step(self):
        self.y -= self.accel*self.step_size
        if self.accel > self.base_accel:
            self.accel -= 2
    def jump(self):
        self.accel = 20


