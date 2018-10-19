import socket
import logging
import asyncio
from . import error
from . import utils

_PORT = 27431

_LOGGER = logging.getLogger('socket')

_is_start = False
_device_list = []
_message_handlers = []
loop = asyncio.get_event_loop()

_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
_sock.setblocking(False)


def send(ip, mac, password, param1, param2):
    if not _is_start:
        start()

    address = (ip, _PORT)
    cmd = 'lan_phone%%%s%%%s%%%s%%%s' % (mac, password, param1, param2)
    message = utils.encrypt(cmd)
    _sock.sendto(message, address)
    _LOGGER.debug('send %s %s', ip, cmd)


async def _do_receive():
    def message_handler(*args):
        message, (address, _) = _sock.recvfrom(256)
        message = utils.decrypt(message)
        _LOGGER.debug('receive %s %s', address, message or '(empty)')

        device, *data = message.split('%')

        if len(data) < 4 or device != 'lan_device':
            _LOGGER.error('incorrect response %s', message)
        else:
            for callback in _message_handlers:
                callback(address, *data)

    loop.add_reader(_sock.fileno(), message_handler, None)
    while True:
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            loop.remove_reader(_sock.fileno())
            break


async def receive(mac=None):
    future = asyncio.Future(loop=loop)

    def message_handler(*data):
        if mac is None or mac == data[1]:
            future.set_result(data)

    _message_handlers.append(message_handler)

    try:
        return await asyncio.wait_for(future, timeout=1)
    except asyncio.TimeoutError:
        raise error.Timeout('connect timeout')
    finally:
        _message_handlers.remove(message_handler)


async def send_message(params, retry=2):
    if retry <= 0:
        raise error.Timeout('connect timeout')

    send(*params)

    while True:
        try:
            data = await receive(params[1])
        except error.Timeout:
            return await send_message(params, retry=retry - 1)

        if data[4][-4] == params[4][0] and data[4][-3:] == 'ack':
            return data


def add_message_handler(handler):
    _message_handlers.append(handler)


def remove_message_handler(handler):
    _message_handlers.remove(handler)


def start():
    global _is_start
    _is_start = True
    asyncio.ensure_future(_do_receive())
