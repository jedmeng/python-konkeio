import socket
import logging
import asyncio
from pykonkeio import utils

_PORT = 27431

_LOGGER = logging.getLogger('mock_socket')


class Socket(object):
    def __init__(self, callback):
        self._sock = None
        self._callback = callback
        self._task = None

    def send(self, address, mac, password, param1, param2):
        cmd = 'lan_device%%%s%%%s%%%s%%%s' % (mac, password, param1, param2)
        message = utils.encrypt(cmd)
        self._sock.sendto(message, address)
        _LOGGER.debug('send %s %s', address[0], cmd)

    async def _do_receive(self, loop=None):
        def message_handler(*args):
            message, address = self._sock.recvfrom(256)
            message = utils.decrypt(message)
            _LOGGER.debug('receive %s %s %s', *address, message or '(empty)')

            device, *data = message.split('%')

            if len(data) < 4 or device != 'lan_phone':
                _LOGGER.error('incorrect request %s', message)
            else:
                self._callback(address, *data)
        loop = loop or asyncio.get_event_loop()
        loop.add_reader(self._sock.fileno(), message_handler, None)

    def open(self, loop=None):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', _PORT))
        self._sock.setblocking(False)
        self._task = asyncio.ensure_future(self._do_receive(loop=loop))

    def close(self):
        self._task.cancel()
        self._sock.close()




