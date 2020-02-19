from motor import Motor
from servo import Servo
import RPi.GPIO as GPIO
import Adafruit_PCA9685

class RaspTank:

    MAX_DUTY_CYCLE = 100

    def __init__(self, motor_left, motor_right, servos):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.motor_left = Motor(motor_left['pwm'], motor_left['pin1'], motor_left['pin2'])
        self.motor_right = Motor(motor_right['pwm'], motor_right['pin2'], motor_right['pin1'])
        self.servo_default = 300
        self.servos = {name: Servo(self.pwm, servo['channel'], servo['max'], servo['min'], self.servo_default) for (name, servo) in servos.items()}
        self.servos_last_change = {name: 0 for name in servos}
        self.thrust = 0
        self.direction = 'forward'
        self.turn_value = 0
        self.pwm.set_all_pwm(0, self.servo_default)

    def handle_event(self, event):
        # self.event_map[event.code](self, event.state)
        self.event_map.get(event.code, RaspTank.stop)(self, event.state)

    def drive(self, direction, thrust):
        # slow down one motor on turn
        print('turn', self.turn_value)
        if self.turn_value > 0:
            turn = abs(self.turn_value)
            self.motor_left.work(direction, round(thrust*(1-turn)))
            self.motor_right.work(direction, thrust)
            return None;

        if self.turn_value < 0:
            turn = abs(self.turn_value)
            self.motor_left.work(direction, thrust)
            self.motor_right.work(direction, round(thrust*(1-turn)))
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

    def stop(self, value):
        pass

    def move_arm_1(self, value):
        servo_value = 0 if value == 0 else (-2 if value > 0 else 2)
        if value > 0 and (self.servos_last_change['arm1'] < value):
            self.servos['arm1'].move(servo_value)
        if value < 0 and (self.servos_last_change['arm1'] > value):
            self.servos['arm1'].move(servo_value)
        self.servos_last_change['arm1'] = value

    def move_arm_2(self, value):
        servo_value = 0 if value == 0 else (2 if value > 0 else -2)
        if value > 0 and (self.servos_last_change['arm2'] < value):
            self.servos['arm2'].move(servo_value)
        if value < 0 and (self.servos_last_change['arm2'] > value):
            self.servos['arm2'].move(servo_value)
        self.servos_last_change['arm2'] = value
        
    def move_arm_3(self, value):
        servo_value = 0 if value == 0 else (30 if value > 0 else -30)
        if value > 0:
            self.servos['arm3'].move(servo_value)
        if value < 0:
            self.servos['arm3'].move(servo_value)
        self.servos_last_change['arm3'] = value
        
    def move_arm_4(self, value):
        servo_value = 0 if value == 0 else (30 if value > 0 else -30)
        if value > 0:
            self.servos['arm4'].move(servo_value)
        if value < 0:
            self.servos['arm4'].move(servo_value)
        self.servos_last_change['arm4'] = value

    def move_front(self, value):
        servo_value = 0 if value == 0 else (-2 if value > 0 else 2)
        if value > 0 and (self.servos_last_change['front'] < value):
            self.servos['front'].move(servo_value)
        if value < 0 and (self.servos_last_change['front'] > value):
            self.servos['front'].move(servo_value)
        self.servos_last_change['front'] = value


    event_map = {
        'ABS_RZ': drive_forward,
        'ABS_Z': drive_backward,
        'ABS_X': turn,
        'ABS_RY': move_arm_1,
        'ABS_RX': move_arm_2,
        'ABS_HAT0X': move_arm_3,
        'ABS_HAT0Y': move_arm_4,
        'ABS_Y': move_front,
        'anything': stop
    }
