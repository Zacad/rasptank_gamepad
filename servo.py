class Servo:
    def __init__(self, pwm, channel, max_pos, min_pos):
        self.pwm = pwm
        self.channel = channel
        self.max = max_pos
        self.min = min_pos

    def move(self, pos):
        print('move')
        self.pwm.set_pwm(self.channel, 0, pos)

    def __str__(self):
        return str(self.pwm)+', '+self.channel+', '+self.max+', '+self.min
