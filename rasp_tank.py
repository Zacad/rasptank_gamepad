from motor import Motor
import RPi.GPIO as GPIO


class RaspTank:

    MAX_DUTY_CYCLE = 100

    def __init__(self, motor_left, motor_right):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.motor_left = Motor(motor_left['pwm'], motor_left['pin1'], motor_left['pin2'])
        self.motor_right = Motor(motor_right['pwm'], motor_right['pin2'], motor_right['pin1'])
        self.thrust = 0
        self.direction = 'forward'
        self.turn_value = 0

    def handle_event(self, event):
        #self.event_map[event.code](self, event.state)
        self.event_map.get(event.code, 'anything')(self, event.state)

    def drive(self, direction, thrust):
        if self.turn_value > 0:
            self.motor_left.work(direction, abs(round(thrust*self.turn_value)))
            self.motor_right.work(direction, thrust)
            return None;

        if self.turn_value < 0:
            self.motor_left.work(direction, thrust)
            self.motor_right.work(direction, abs(round(thrust*self.turn_value)))
            return None;

        self.motor_left.work(direction, thrust)
        self.motor_right.work(direction, thrust)

    def drive_forward(self, thrust):
        self.thrust = round(thrust*RaspTank.MAX_DUTY_CYCLE) if round(thrust*RaspTank.MAX_DUTY_CYCLE) <= RaspTank.MAX_DUTY_CYCLE else RaspTank.MAX_DUTY_CYCLE
        self.direction = 'forward'
        self.drive(self.direction, self.thrust)

    def drive_backward(self, thrust):
        self.thrust = round(thrust*RaspTank.MAX_DUTY_CYCLE) if round(thrust*RaspTank.MAX_DUTY_CYCLE) <= RaspTank.MAX_DUTY_CYCLE else RaspTank.MAX_DUTY_CYCLE
        self.direction = 'backward'
        self.drive(self.direction, self.thrust)

    def turn(self, value):
        self.turn_value = value
        self.drive(self.direction, self.thrust)

    def stop(self):
        pass

    def move_arm_1(self, value):
        pass

    event_map = {
        'ABS_RZ': drive_forward,
        'ABS_Z': drive_backward,
        'ABS_X': turn,
        'anything': stop
    }
