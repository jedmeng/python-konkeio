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
        _LOGGER.debug('mock server: %s %s %s', self.__class__.__name__, self.mac, self.password)

    def set_is_online(self, is_online):
        self.online = is_online

    def send_message(self, src, action, action_type, password='nopassword'):
        self.socket.send(src, self.mac, password, action, action_type)

    def _message_handler(self, src, mac, password, action, action_type):
        if not self.online:
            return
        elif action_type == 'heart':
            self.send_message(src, password=self.password, action='#', action_type='hack')
        elif mac == self.mac:
            self.message_handler(src, action, action_type)

    def message_handler(self, src, action, device_type):
        pass

    def start(self, loop=None):
        self.socket.open(loop=loop)

    def stop(self):
        print("\n\nmock stop\n\n")
        self.socket.close()
