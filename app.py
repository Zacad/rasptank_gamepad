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

tank = RaspTank(motor_left, motor_right)

while True:
    events = get_gamepad()
    for event in events:
        if event.ev_type == 'Sync':
            continue
        #print(event.ev_type, event.code, event.state)
        event = gamepad.handle_event(event)
        print(event)
        tank.handle_event(event)
