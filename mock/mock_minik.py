import time
from .mock_base_device import MockBaseDevice


class MockMiniK(MockBaseDevice):
    def __init__(self, init_status='close', online=True, is_pro=True):
        super().__init__(online=online)
        self.status = init_status
        self.is_pro = is_pro
        self.learn_start = None

    def heart_response(self):
        if self.is_pro:
            return '%s#%s#%s' % (self.status, 'hv2.0.3', 'sv2.0.7')
        else:
            return '%s#%s#%s' % (self.status, 'hv1.0.3', 'sv1.0.7')

    def message_handler(self, src, action, device_type):
        if action == 'check' and device_type == 'relay':
            self.send_message(src, self.status, 'rack')
        elif action in ['open', 'close'] and device_type == 'relay':
            self.status = action
            self.send_message(src, self.status, 'rack')
        elif action.startswith('operate#3031') and device_type == 'uart':
            self.send_message(src, action, 'uack')
            if action.startswith('operate#3031#learn'):
                self.learn_start = time.time()
            elif action == 'operate#3031#quit':
                self.learn_start = None
        elif action.startswith('check#3031') and device_type == 'uart':
            if time.time() - time.time() < 2:
                self.send_message(src, action, 'uack')
            elif action.endswith('0'):
                self.send_message(src, action + '#failed', 'uack')
            else:
                self.send_message(src, action + '#ok', 'uack')

        if self.is_pro:
            print("device: %s learning: %s" % (self.status, self.learn_start))
        else:
            print("device: %s" % self.status)

    def error_message_handler(self, src, mac, password, action, action_type):
        self.send_message(src, action=action, action_type=action_type, mac=mac, password=password, msg_type='lan_phone')
