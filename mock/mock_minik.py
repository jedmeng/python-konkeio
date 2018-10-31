from .mock_base_device import MockBaseDevice


class MockMiniK(MockBaseDevice):
    def __init__(self, init_status='close', online=True):
        super().__init__(online=online)
        self.status = init_status

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'relay':
            self.send_message(src, self.status, 'rack')
        elif action in ['open', 'close'] and device_type == 'relay':
            self.status = action
            self.send_message(src, self.status, 'rack')

    def error_message_handler(self, src, mac, password, action, action_type):
        self.send_message(src, action=action, action_type=action_type, mac=mac, password=password, msg_type='lan_phone')
