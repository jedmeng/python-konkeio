from .mock_base_device import MockBaseDevice


class MockBaseToggle(MockBaseDevice):
    def __init__(self, ip, device_type='relay', init_status='close'):
        super().__init__(ip, device_type)
        self.type = []
        self.status = init_status

    def message_handler(self, action, value, device_type):
        if action == 'check' and device_type == self.device_type:
            self.send_message(self.status, 'rack')
        elif action in ['open', 'close'] and device_type == self.device_type:
            self.status = action
            self.send_message(self.status, 'rack')
