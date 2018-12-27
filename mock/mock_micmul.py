from .mock_base_device import MockBaseDevice

SOCKET_COUNT = 4


class MockMicMul(MockBaseDevice):
    def __init__(self, init_status=['close'] * SOCKET_COUNT, online=True):
        super().__init__(online=online)
        self.status = list(init_status or ['close'] * SOCKET_COUNT)

    def do_response(self, src):
        open_status = ','.join('%s%d' % (val, index + 1) for index, val in enumerate(self.status))
        lock_status = ','.join('unlock%d' % (index + 1) for index, _ in enumerate(self.status))
        status = '%s,%s' % (open_status, lock_status)
        self.send_message(src, status, 'rack')

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'relay':
            self.do_response(src)
        elif action[0:-1] in ['open', 'close'] and device_type == 'relay':
            index = int(action[-1]) - 1
            self.status[index] = action[0:-1]
            self.do_response(src)
        elif action in ['openall', 'closeall']:
            self.status = list(action[0:-3] for _ in self.status)
            self.do_response(src)

        print("status: %s" % ', '.join(self.status))
