import string
import random
import logging
from .mock_socket import Socket

_LOGGER = logging.getLogger('mock_device')


class MockBaseDevice(object):

    def __init__(self, mac=None, password=None, online=False):
        self.mac = mac or '-'.join(map(lambda x: '%0.2x' % random.randint(0, 255), range(6)))
        self.password = password or ''.join(map(lambda x: random.choice(string.ascii_uppercase), range(8)))
        self.online = online
        self.socket = Socket(self._message_handler)
        self._send_flag = False
        _LOGGER.debug('mock server: %s %s %s', self.__class__.__name__, self.mac, self.password)

    def set_is_online(self, is_online):
        self.online = is_online

    def send_message(self, src, action=None, action_type=None, mac=None, password='nopassword', **kwargs):
        self._send_flag = True
        self.socket.send(src, mac=mac or self.mac, password=password, action=action, action_type=action_type, **kwargs)

    def _message_handler(self, src, mac, password, action, action_type):
        self._send_flag = False
        if not self.online:
            return
        elif action_type == 'heart':
            self.send_message(src, password=self.password, action='#', action_type='hack')
        elif mac == self.mac:
            self.message_handler(src, action, action_type)

        if not self._send_flag:
            self.error_message_handler(src, mac, password, action, action_type)

    def error_message_handler(self, src, mac, password, action, action_type):
        self.send_message(src)

    def message_handler(self, src, action, device_type):
        pass

    def start(self, loop=None):
        self.socket.open(loop=loop)

    def stop(self):
        self.socket.close()
