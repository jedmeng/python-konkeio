from .mock_base_device import MockBaseDevice

SOCKET_COUNT = 4


class MockMicMul(MockBaseDevice):
    def __init__(self, init_status=['close'] * SOCKET_COUNT, online=True):
        super().__init__(online=online)
        self.status = list(init_status or ['close'] * SOCKET_COUNT)

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

        print("status: %s" % ', '.join(self.status))
