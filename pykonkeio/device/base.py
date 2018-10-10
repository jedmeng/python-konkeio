from .. import manager
from .. import error

PORT = 27431


class BaseDevice(object):

    def __init__(self, ip, device_type):
        self.manager = manager.Manager.get_instance()
        self.ip = ip
        self.device_type = device_type
        self.mac = None
        self.password = None
        self.online = False

    def fetch_info(self):
        t = self.manager.get_device(self.ip)

        if t is None:
            self.online = False
        else:
            self.online = True
            _, self.mac, self.password, *_ = t

    def send_message(self, action, message_type=None, retry=2):
        if not self.online:
            self.fetch_info()

        if not self.online:
            raise error.DeviceOffline('device is offline')

        if retry <= 0:
            raise error.Timeout('connect timeout')

        self.manager.send(self.ip, self.mac, self.password, action, message_type or self.device_type)

        while True:
            try:
                ip, mac, _, action, device_type = self.manager.receive()
            except error.Timeout:
                return self.send_message(action, retry=retry - 1)

            if mac == self.mac and device_type[-3:] == 'ack':
                return action

    def do(self, action, value=None):
        raise error.IllegalAction()
