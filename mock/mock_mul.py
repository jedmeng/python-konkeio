from .mock_base_device import MockBaseDevice

SOCKET_COUNT = 3
USB_COUNT = 2


class MockMul(MockBaseDevice):
    def __init__(self, init_status=None, usb_status=None, online=True):
        super().__init__(online=online)
        self.status = list(init_status or ['close'] * SOCKET_COUNT)
        self.usb_status = list(usb_status or ['close'] * USB_COUNT)

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'relay':
            status = ','.join('%s%d' % (val, index + 1) for index, val in enumerate(self.status))
            self.send_message(src, status, 'rack')
        elif action[0:-1] in ['open', 'close'] and device_type == 'relay':
            index = int(action[-1]) - 1
            self.status[index] = action[0:-1]
            self.send_message(src, self.status[index], 'rack')
        elif action in ['openall', 'closeall']:
            self.status = list(action[0:-3] for _ in self.status)
            self.send_message(src, 'x', 'rack')
        elif action == 'check' and device_type == 'usb':
            status = ','.join('%s%d' % (val, index + 1) for index, val in enumerate(self.usb_status))
            self.send_message(src, status, 'uack')
        elif action[0:-1] in ['open', 'close'] and device_type == 'usb':
            index = int(action[-1]) - 1
            self.usb_status[index] = action[0:-1]
            self.send_message(src, self.usb_status[index], 'uack')

        print("status: %s usb_status: %s" % (', '.join(self.status), ', '.join(self.usb_status)))
