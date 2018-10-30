from .mock_base_device import MockBaseDevice


class MockKLight(MockBaseDevice):
    def __init__(self, init_status='close', init_brightness=0, init_color=(0, 0, 0), online=True):
        super().__init__(online=online)
        self.status = init_status
        self.brightness = init_brightness
        self.color = init_color

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'klight':
            r, g, b = self.color
            status = '%s#x#x#x#x#1,x#1&#%d#%d#%d#%d#2,x#1&#x#x#x#x#3,x#1&#x#x#x#x#5,x#1' % \
                     (self.status, int(r), int(g), int(b), int(self.brightness))
            self.send_message(src, status, 'klack')
        elif action in ['open', 'close'] and device_type == 'klight':
            self.status = action
            self.send_message(src, self.status, 'klack')
        elif action[0:3] == 'set' and device_type == 'klight':
            _, r, g, b, brightness, *_ = action.split('#')
            self.color = (r, g, b)
            self.brightness = brightness
            self.send_message(src, 'x', 'klack')

