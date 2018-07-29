import argparse
import socket
import time
import re

from . import utils

PORT = 27431

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.settimeout(3)

device_list = {}


class KonekeDevice(object):

    def __init__(self, ip, mac, password, device):
        self.ip = ip
        self.mac = mac
        self.password = password
        self.device = device
        self.online = True

    @staticmethod
    def send(ip, mac, password, param1, param2):
        address = (ip, PORT)
        cmd = 'lan_phone%{}%{}%{}%{}'.format(mac, password, param1, param2)
        message = utils.encrypt(cmd)
        s.sendto(message, address)
        # print('send', cmd)

    @staticmethod
    def receive():
        data, address = s.recvfrom(128)

        incoming_message = utils.decrypt(data)
        # print('receive', incoming_message)

        _, mac, password, action, device_type = incoming_message.split('%')
        ip, port = address
        return ip, mac, password, action, device_type

    """
        搜索设备
        req: lan_phone%mac%nopassword%2018-04-21-16:26:04%heart
        res: lan_device%28-d9-8a-xx-xx-xx%XXXXXXXX%close#hv2.0.3#sv2.0.7%hack
    """
    @staticmethod
    def search(ip='255.255.255.255', callback=None):
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        KonekeDevice.send(ip, 'mac', 'nopassword', datetime, 'heart')

        while True:
            try:
                result = KonekeDevice.receive()
            except socket.timeout:
                break

            if callback is not None:
                callback(*result)

            device_list[result[0]] = result

    def send_message(self, action, retry=3):
        if retry <= 0:
            raise socket.timeout

        self.send(self.ip, self.mac, self.password, action, self.device)

        while True:
            try:
                ip, mac, _, action, device_type = self.receive()
            except socket.timeout:
                return self.send_message(action, retry-1)

            if mac == self.mac and device_type == 'rack':
                break

        return action

    def fetch_info(self):
        if self.ip not in device_list:
            self.search()

        # 特殊情况下广播包可能被屏蔽
        if self.ip not in device_list:
            self.search(self.ip)

        if self.ip not in device_list:
            raise socket.error

        ip, mac, password, action, device_type = device_list[self.ip]

        self.mac = mac
        self.password = password

        return action, device_type


class Switch(KonekeDevice):

    def __init__(self, ip, mac=None, password=None):
        self.status = 'offline'
        super(Switch, self).__init__(ip, mac, password, 'relay')
        self.update()

    def update(self):
        if self.mac is None or self.password is None:
            self.fetch_info()
        else:
            self.check()

    def fetch_info(self):
        try:
            action, device_type = super(Switch, self).fetch_info()
            self.status = re.sub(r'#.*$', "", action)
        except socket.error:
            self.online = False
            self.status = 'offline'

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """
    def check(self):
        try:
            result = self.send_message('check')
            self.online = True
            self.status = result
        except socket.error:
            self.online = False
            self.status = 'offline'

        return self.status

    """
        打开开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """
    def turn_on(self):
        if self.online is False:
            return False
        elif self.status == 'open':
            return True

        result = self.send_message('open')
        self.status = result

        return result == 'open'

    """
        打开开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """
    def turn_off(self):
        if self.online is False:
            return False
        elif self.status == 'close':
            return True

        result = self.send_message('close')
        self.status = result

        return result == 'close'


def print_device(ip, mac, password):
    print('ip: %s\nmac: %s\npassword: %s\n\n' % (ip, mac, password))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='open, close, check or search')
    parser.add_argument('-a', '--address', help='device ip address', default='255.255.255.255')
    parser.add_argument('-d', '--device', help='currently "switch" only', default='switch')

    args = parser.parse_args()

    if args.action == 'search':
        try:
            KonekeDevice.search(ip=args.address, callback=print_device)
        except socket.error:
            print('search timeout')
    else:
        if args.address is None:
            print('IP address is empty.')
            return

        if args.device == 'switch':
            device = Switch(args.address)
        else:
            print('device %s not support' % args.device)
            return

        if args.action == 'check':
            print('status: %s' % device.status)
        elif args.action == 'open':
            if device.turn_on():
                print('Turn on success')
            else:
                print('Turn on failed')

        elif args.action == 'close':
            if device.turn_off():
                print('Turn off success')
            else:
                print('Turn off failed')
        else:
            print('action is illegal.')

    exit(0)


if __name__ == "__main__":
    main()
