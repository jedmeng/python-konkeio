import time
import logging
import asyncio

from . import error
from . import socket
from .device import *

_LOGGER = logging.getLogger(__name__)
_devices = {}
_device_info = {}


async def search(ip='255.255.255.255', callback=None, loop=None):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    socket.send(ip, 'mac', 'nopassword', datetime, 'heart')

    future = asyncio.Future(loop=loop)

    def message_handler(*data):
        if data[4] != 'hack':
            return
        if callback is not None:
            callback(*data)
        if ip == data[0] and not future.done():
            future.set_result(data)
            _device_info[data[0]] = data

    socket.add_message_handler(message_handler)
    try:
        return await asyncio.wait_for(future, timeout=2)
    except asyncio.TimeoutError:
        raise error.Timeout
    finally:
        socket.remove_message_handler(message_handler)


def get_device(ip, device_type=None):
    if ip in _devices:
        return _devices[ip]

    if device_type is None:
        device = BaseToggle(ip)
    elif device_type == 'k2':
        device = K2(ip)
    elif device_type == 'minik':
        device = MiniK(ip)
    elif device_type == 'micmul':
        device = MicMul(ip)
    elif device_type == 'mul':
        device = Mul(ip)
    elif device_type == 'klight':
        device = KLight(ip)
    elif device_type == 'kbulb':
        device = KBulb(ip)
    else:
        raise error.IllegalDevice('device %s not support' % device_type)

    _devices[ip] = device
    return device


def clear_device_info(ip=None):
    global _device_info
    if ip:
        del _device_info[ip]
    else:
        _device_info = {}


async def get_device_info(ip):
    if ip not in _device_info:
        await search(ip)
    return _device_info[ip]
