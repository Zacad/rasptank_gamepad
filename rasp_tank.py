from motor import Motor
import RPi.GPIO as GPIO


class RaspTank:

    MAX_DUTY_CYCLE = 100

    def __init__(self, motor_left, motor_right):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.motor_left = Motor(motor_left['pwm'], motor_left['pin1'], motor_left['pin2'])
        self.motor_right = Motor(motor_right['pwm'], motor_left['pin1'], motor_left['pin2'])
        self.thrust = 0
        self.turn = 0

    def handle_event(self, event):
        RaspTank.event_map[event.code](event.state)

    def drive(self, direction, thrust):
        self.motor_left.work(direction, thrust)
        self.motor_right.work(direction, thrust)

    def drive_forward(self, thrust):
        self.thrust = round(thrust*RaspTank.MAX_DUTY_CYCLE) if round(thrust*RaspTank.MAX_DUTY_CYCLE) <= RaspTank.MAX_DUTY_CYCLE else RaspTank.MAX_DUTY_CYCLE
        self.drive('forward', self.thrust)

    def drive_backward(self, thrust):
        self.thrust = round(thrust*RaspTank.MAX_DUTY_CYCLE) if round(thrust*RaspTank.MAX_DUTY_CYCLE) <= RaspTank.MAX_DUTY_CYCLE else RaspTank.MAX_DUTY_CYCLE
        self.drive('backward', self.thrust)

    def turn(self, direction, value):
        pass

    def stop(self):
        pass

    def move_arm_1(self, value):
        pass

    event_map = {
        'ABS_RZ': drive_forward(),
        'ABS_Z': drive_backward()
    }
