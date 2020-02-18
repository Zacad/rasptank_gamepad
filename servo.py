import time

class Servo:
    def __init__(self, pwm, channel, max_pos, min_pos, default):
        self.pwm = pwm
        self.channel = channel
        self.max = max_pos
        self.min = min_pos
        self.value = default if self.min < default < self.max else self.min

    def move(self, pos):
        pos = self.value + pos
        if pos > self.max:
            pos = self.max
        if pos < self.min:
            pos = self.min
        self.pwm.set_pwm(self.channel, 0, pos)
        self.value = pos

    def __str__(self):
        return str(self.pwm)+', '+str(self.channel)+', '+str(self.max)+', '+str(self.min)
