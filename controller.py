
class Controller:
    analog_codes = ['ABS_X', 'ABS_Y', 'ABS_RX', 'ABS_RY']
    trigger_codes = ['ABS_Z', 'ABS_RZ']

    TRIGGER_MAX = 255
    TRIGGER_MIN = 0

    ANALOG_MAX = 32768
    ANALOG_MIN = -32768

    def handle_event(self, event):
        if event.code in Controller.analog_codes:
            event.state = Controller.normalize_analog(event)
        if event.code in Controller.trigger_codes:
            event.state = Controller.normalize_trigger(event)

        print(event.code, event.state)
        return event

    def normalize_trigger(event):
        return round(event.state/Controller.TRIGGER_MAX, 2)


    def normalize_analog(event):
        return round(event.state/Controller.ANALOG_MAX, 2) * -1
