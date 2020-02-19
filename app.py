from inputs import get_gamepad
from controller import Controller
from rasp_tank import  RaspTank

gamepad = Controller()

# robot initialization
motor_left = {
    'pwm': 4,
    'pin1': 14,
    'pin2': 15
}
motor_right = {
    'pwm': 17,
    'pin1': 27,
    'pin2': 18
}

servos = {
    'arm1': {
        'channel': 12,
        'min': 100,
        'max': 430
    },
    'arm2': {
        'channel': 13,
        'min': 100,
        'max': 430
    },
    'arm3': {
        'channel': 14,
        'min': 150,
        'max': 450
    },
    'arm4': {
        'channel': 15,
        'min': 100,
        'max': 301
    },
}

tank = RaspTank(motor_left, motor_right, servos)

while True:
    events = get_gamepad()
    for event in events:
        if event.ev_type == 'Sync':
            continue
        event = gamepad.handle_event(event)
        tank.handle_event(event)
