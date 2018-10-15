import socket
import time
import logging

from . import error
from . import utils

PORT = 27431

logger = logging.getLogger('konkeio')


class Manager:
    instance = None

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.settimeout(3)
        self.device_list = {}

    def send(self, ip, mac, password, param1, param2):
        address = (ip, PORT)
        cmd = 'lan_phone%%%s%%%s%%%s%%%s' % (mac, password, param1, param2)
        message = utils.encrypt(cmd)
        self.s.sendto(message, address)
        logger.debug('send %s', cmd)

    def receive(self):
        try:
            data, address = self.s.recvfrom(128)
        except socket.timeout:
            raise error.Timeout

        incoming_message = utils.decrypt(data)
        logger.debug('receive %s', incoming_message or '(empty)')

        if len(incoming_message.split('%')) != 5:
            logger.error('incorrect response %s', incoming_message)
            return None

        sender, mac, password, action, device_type = incoming_message.split('%')

        if sender != 'lan_device':
            return self.receive()

        ip, _ = address
        return ip, mac, password, action, device_type

    """
        搜索设备
        req: lan_phone%mac%nopassword%2018-04-21-16:26:04%heart
        res: lan_device%28-d9-8a-xx-xx-xx%XXXXXXXX%close#hv2.0.3#sv2.0.7%hack
    """
    def search(self, ip='255.255.255.255', callback=None):
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.send(ip, 'mac', 'nopassword', datetime, 'heart')
        self.send(ip, 'mac', 'nopassword', datetime, 'heart')

        while True:
            try:
                result = self.receive()
            except socket.timeout:
                break

            if callback is not None:
                callback(*result)

            self.device_list[result[0]] = result

            if result[0] == ip:
                break

    def get_device(self, ip):
        if ip in self.device_list:
            return self.device_list[ip]

        self.search(ip)
        return self.device_list[ip]

    @staticmethod
    def get_instance():
        if Manager.instance is None:
            Manager.instance = Manager()
        return Manager.instance
