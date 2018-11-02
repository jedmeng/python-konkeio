from .. import manager
from .. import socket
from .. import error


class BaseDevice(object):

    def __init__(self, ip, device_type, loop=None):
        self.ip = ip
        self.device_type = device_type
        self.mac = None
        self.password = None
        self.is_online = False
        self.loop = loop

    async def fetch_info(self):
        try:
            self.is_online = True
            _, self.mac, self.password, status, _ = await manager.get_device_info(self.ip)
            return status
        except error.Timeout:
            self.is_online = False

    async def send_message(self, action, action_type=None, retry=2, loop=None):
        if not self.is_online:
            await self.fetch_info()

        if not self.is_online:
            raise error.DeviceOffline('device is offline')

        params = (self.ip, self.mac, self.password, action, action_type or self.device_type)

        try:
            data = await socket.send_message(params, retry=retry, loop=loop or self.loop)
            return data[3]
        except error.Timeout:
            self.is_online = False
            raise error.DeviceOffline('device is offline')

    async def do(self, action, value=None):
        raise error.IllegalAction()
