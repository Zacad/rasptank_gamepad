class Servo:
    def __init__(self, pwm, channel, max_pos, min_pos):
        self.pwm = pwm
        self.channel = channel
        self.max = max_pos
        self.min = min_pos

    def move(self, pos):
        self.pwm.set_pwm(self.channel, 0, pos)
