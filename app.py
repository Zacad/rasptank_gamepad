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
        'min': 430,
        'max': 100
    },
    'arm2': {
        'channel': 13,
        'min': 430,
        'max': 300
    },
    'arm3': {
        'channel': 14,
        'min': 430,
        'max': 300
    },
    'arm4': {
        'channel': 15,
        'min': 430,
        'max': 300
    },
}

tank = RaspTank(motor_left, motor_right, servos)

while True:
    events = get_gamepad()
    for event in events:
        if event.ev_type == 'Sync':
            continue
        #print(event.ev_type, event.code, event.state)
        event = gamepad.handle_event(event)
        print(event)
        tank.handle_event(event)
