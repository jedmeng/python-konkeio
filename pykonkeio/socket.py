import socket
import math
import logging
import asyncio
from . import error
from . import utils

_PORT = 27431

_LOGGER = logging.getLogger(__name__)

_requests = []
_receivers_count = 0
_message_handlers = []
_receive_task = None

_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
_sock.setblocking(False)


def send(ip, mac, password, action, action_type, device_type='lan_phone'):
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
            return _LOGGER.error('incorrect response %s', message)

        mac, _, _, response_type = data

        for request in _requests:
            if not request['future'].done() and request['mac'] == mac and request['request_type'].startswith(response_type[:-3]):
                request['future'].set_result((address, *data))
                break

        for callback in _message_handlers:
            callback(address, *data)

    loop = loop or asyncio.get_event_loop()
    loop.add_reader(_sock.fileno(), message_handler, None)

    try:
        await asyncio.sleep(math.inf)
    except asyncio.CancelledError:
        loop.remove_reader(_sock.fileno())


async def send_message(params, retry=2, loop=None, **kwargs):
    request = {
        'mac': params[1],
        'request_type': params[4],
        'future': asyncio.Future(loop=loop)
    }
    _requests.append(request)

    send(*params)
    add_receiver(loop=loop)

    try:
        return await asyncio.wait_for(request['future'], timeout=1)
    except asyncio.TimeoutError:
        if retry > 0:
            return await send_message(params, retry=retry-1, loop=loop)
        raise error.Timeout('connect timeout')
    finally:
        _requests.remove(request)
        remove_receiver()


def add_message_handler(handler, loop=None):
    _message_handlers.append(handler)
    add_receiver(loop=loop)


def remove_message_handler(handler):
    _message_handlers.remove(handler)
    remove_receiver()


def add_receiver(loop=None):
    global _receivers_count, _receive_task
    if _receivers_count == 0:
        _receive_task = asyncio.ensure_future(_do_receive(loop=loop))
    _receivers_count += 1


def remove_receiver():
    global _receivers_count
    _receivers_count -= 1
    if _receivers_count == 0:
        _receive_task and _receive_task.cancel()
