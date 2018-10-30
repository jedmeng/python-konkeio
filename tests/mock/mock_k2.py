import random
from .mock_base_device import MockBaseDevice


class MockK2(MockBaseDevice):
    def __init__(self, init_status='close', init_light_status='close', init_usb_status='close', online=True):
        super().__init__(online=online)
        self.status = init_status
        self.light_status = init_light_status
        self.usb_status = init_usb_status
        self.last_power = 0

    def message_handler(self, src, action, device_type):
        print('action %s device_type %s', action, device_type)
        if action == 'check' and device_type == 'relay':
            self.send_message(src, self.status, 'rack')
        elif action in ['open', 'close'] and device_type == 'relay':
            self.status = action
            self.send_message(src, self.status, 'rack')
        elif action == 'check' and device_type == 'light':
            self.send_message(src, self.light_status, 'lack')
        elif action in ['open', 'close'] and device_type == 'light':
            self.light_status = action
            self.send_message(src, self.light_status, 'lack')
        elif action == 'check' and device_type == 'usb':
            self.send_message(src, self.usb_status, 'uack')
        elif action in ['open', 'close'] and device_type == 'usb':
            self.usb_status = action
            self.send_message(src, self.usb_status, 'uack')
        elif action == 'check' and device_type == 'power':
            self.last_power = random.randint(0, 3000) / 100
            power = 'dl_module#power#%.2f' % self.last_power
            self.send_message(src, power, 'pack')

