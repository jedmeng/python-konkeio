from .mock_base_device import MockBaseDevice


class MockKBulb(MockBaseDevice):
    def __init__(self, init_status='close', init_brightness=0, init_ct=2700, online=True):
        super().__init__(online=online)
        self.status = init_status
        self.brightness = init_brightness
        self.ct = init_ct

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'kbulb':
            status = '%s#%s,%s,1&&' % (self.status, self.ct, self.brightness)
            self.send_message(src, status, 'kback')
        elif action in ['open', 'close'] and device_type == 'kbulb':
            self.status = action
            self.send_message(src, self.status, 'kback')
        elif action[0:3] == 'set' and device_type == 'kbulb':
            _, name, value = action.split('#')
            if name == 'lum':
                self.brightness = value
            elif name == 'ctp':
                self.ct = value
            self.send_message(src, action, 'kback')
            self.status = 'open'
