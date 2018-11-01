import socket
import math
import logging
import asyncio
from . import error
from . import utils

_PORT = 27431

_LOGGER = logging.getLogger('socket')

_is_start = False
_device_list = []
_message_handlers = []
_receive_task = None

_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
_sock.setblocking(False)


def send(ip, mac, password, action, action_type, device_type='lan_phone', loop=None):
    if not _is_start:
        start(loop=loop)

    address = (ip, _PORT)
    cmd = '%s%%%s%%%s%%%s%%%s' % (device_type, mac, password, action, action_type)
    message = utils.encrypt(cmd)
    _sock.sendto(message, address)
    _LOGGER.debug('send %s %s', ip, cmd)


async def _do_receive(loop=None):
    def message_handler(*_):
        message, (address, _) = _sock.recvfrom(256)
        message = utils.decrypt(message)
        _LOGGER.debug('receive %s %s', address, message or '(empty)')

        device, *data = message.split('%')

        if len(data) < 4 or device != 'lan_device':
            _LOGGER.error('incorrect response %s', message)
        else:
            for callback in _message_handlers:
                callback(address, *data)

    loop = loop or asyncio.get_event_loop()
    loop.add_reader(_sock.fileno(), message_handler, None)
    try:
        await asyncio.sleep(math.inf)
    except asyncio.CancelledError:
        loop.remove_reader(_sock.fileno())


async def receive(mac=None, loop=None):
    if not _is_start:
        start(loop=loop)
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
        if len(_message_handlers) == 0:
            stop()


async def send_message(params, retry=2, loop=None):
    if retry <= 0:
        raise error.Timeout('connect timeout')

    send(*params, loop=loop)

    while True:
        try:
            data = await receive(params[1], loop=loop)
        except error.Timeout:
            return await send_message(params, retry=retry - 1, loop=loop)

        if data[4][0] == params[4][0] and data[4][-3:] == 'ack':
            return data


def add_message_handler(handler):
    _message_handlers.append(handler)


def remove_message_handler(handler):
    _message_handlers.remove(handler)


def start(loop=None):
    global _is_start, _receive_task
    _is_start = True
    _receive_task = asyncio.ensure_future(_do_receive(loop=loop))


def stop():
    global _is_start, _receive_task
    _is_start = False
    _receive_task and _receive_task.cancel()
