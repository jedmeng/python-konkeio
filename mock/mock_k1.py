from .mock_base_device import MockBaseDevice
import random


class MockK1(MockBaseDevice):
    def __init__(self, init_status='close', online=True):
        super().__init__(online=online)
        self.status = init_status
        self.mac = self.mac.replace('-', ':')
        self.password = 'nopassword'
        self.actions = {}

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'request':
            self.send_message(src, self.status, 'rack')
        elif action in ['open', 'close'] and device_type == 'request':
            code = '%05d' % random.randint(0, 99999)
            self.actions[code] = action
            self.send_message(src, 'confirm#%s' % code, 'rack')
        elif action[0:7] == 'confirm':
            self.status = self.actions[action[8:]]
            self.send_message(src, self.status, 'rack')

        print("device: %s" % self.status)
