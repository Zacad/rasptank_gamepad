import RPi.GPIO as GPIO

class Motor:
    def __init__(self, pin_pwm, pin1, pin2):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        GPIO.setup(pin_pwm, GPIO.OUT)
        self.pin_pwm = pin_pwm
        self.pin_1 = pin1
        self.pin_2 = pin2
        self.pwm = GPIO.PWM(pin_pwm, 1000)
        self.stop()

    def work(self, direction, speed):
        # zero is minimum speed
        if speed < 0:
            speed = 0

        # 100 is maximum speed
        if speed > 100:
            speed = 100

        # below 60 the current is too small to power motor
        if 0 < speed < 60:
            speed = 60

        if direction == 'forward':
            GPIO.output(self.pin_1, GPIO.HIGH)
            GPIO.output(self.pin_2, GPIO.LOW)
            self.pwm.start(0)
            self.pwm.ChangeDutyCycle(speed)

        if direction == 'backward':
            GPIO.output(self.pin_1, GPIO.LOW)
            GPIO.output(self.pin_2, GPIO.HIGH)
            self.pwm.start(0)
            self.pwm.ChangeDutyCycle(speed)
        print(speed)

    def stop(self):
        GPIO.output(self.pin_1, GPIO.LOW)
        GPIO.output(self.pin_2, GPIO.LOW)
        GPIO.output(self.pin_pwm, GPIO.LOW)

    def __del__(self):
        self.stop()
        GPIO.cleanup()             # Release resource
