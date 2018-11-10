import time
import random
from .mock_base_device import MockBaseDevice


class MockK2(MockBaseDevice):
    def __init__(self, init_status='close', init_light_status='close', init_usb_status='close', ir_module=True,
                 rf_module=True, online=True):
        super().__init__(online=online)
        self.status = init_status
        self.light_status = init_light_status
        self.usb_status = init_usb_status
        self.last_power = 0
        self.ir_module = ir_module
        self.rf_module = rf_module
        self.ir_learn_start = None
        self.rf_learn_start = None

    def heart_response(self):
        cmd = self.status + '#'
        if self.ir_module:
            cmd += 'ir_module#on#'
        if self.rf_module:
            cmd += 'rf_module#on#'
        return cmd[0:-1]

    def message_handler(self, src, action, device_type):
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
        elif action.startswith('operate#3031') and device_type == 'uart':
            self.send_message(src, action, 'uack')
            if action.startswith('operate#3031#learn'):
                self.ir_learn_start = time.time()
            elif action == 'operate#3031#quit':
                self.ir_learn_start = None
        elif action.startswith('check#3031') and device_type == 'uart':
            if time.time() - time.time() < 2:
                self.send_message(src, action, 'uack')
            elif action.endswith('0'):
                self.send_message(src, action + '#failed', 'uack')
            else:
                self.send_message(src, action + '#ok', 'uack')
        elif action.startswith('operate#3035') and device_type == 'uart':
            self.send_message(src, action, 'uack')
            if action.startswith('operate#3035#learn'):
                self.rf_learn_start = time.time()
            elif action == 'operate#3035#quit':
                self.rf_learn_start = None
        elif action.startswith('check#3035') and device_type == 'uart':
            if time.time() - time.time() < 2:
                self.send_message(src, action, 'uack')
            elif action.endswith('0'):
                self.send_message(src, action + '#failed', 'uack')
            else:
                self.send_message(src, action + '#ok', 'uack')

        print("device: %s usb: %s light: %s" % (self.status, self.usb_status, self.light_status))
