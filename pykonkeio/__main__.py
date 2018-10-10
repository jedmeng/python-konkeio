import argparse
import logging

from . import manager
from . import error
from .device import *

logging.basicConfig(level=logging.WARN,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s %(levelname)s %(message)s')

example = '''
usage: konkeio [action] [device] [address] [value] [--verbose]

Supported devices and actions supported by each device:
global: search
k2:     get_status turn_[on/off] turn_[on/off]_usb turn_[on/off]_light
minik:  get_status turn_[on/off]
micmul: get_count get_status_all get_status[1/2/3/4] turn_[on/off]_all turn_[on/off]_socket[1/2/3/4]
mul:    get_count get_status_all get_status[1/2/3] get_usb_count get_usb_status_all get_usb_status[1/2] 
        turn_[on/off]_all turn_[on/off]_socket[1/2/3] turn_[on/off]_usb[1/2] 
klight: get_status get_brightness get_color turn_[on/off] set_brightness set_color
kblub:  get_status get_brightness get_ct turn_[on/off] set_brightness set_ct

* each action starts with 'set_' must provide a value parameter
value format:
color:      r,g,b
ct:         2700-6500
brightness: 0-100

example:
konkeio search
konkeio turn_on minik 192.168.0.64
konkeio get_status minik 192.168.0.64
konkeio turn_on_usb k2 192.168.0.64
konkeio turn_off_light k2 192.168.0.64
konkeio get_count micmul 192.168.0.64
konkeio turn_on_socket3 micmul 192.168.0.64
konkeio get_status2 mul 192.168.0.64
konkeio turn_off_all mul 192.168.0.64
konkeio get_brightness klight 192.168.0.64
konkeio set_color klight 192.168.0.64 255,255,0
konkeio set_ct blub 192.168.0.64 3400
konkeio turn_off bulb 192.168.0.64
'''


def print_device(ip, mac, password, action, device_type):
    print('ip: %s\nmac: %s\npassword: %s\n\n' % (ip, mac, password))


def main():
    parser = argparse.ArgumentParser(prog="konkeio", epilog=example,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', help='action name')
    parser.add_argument('device', help='device type')
    parser.add_argument('address', help='device ip address', nargs='?')
    parser.add_argument('value', help='action value', nargs='?')
    parser.add_argument('-v', dest='verbose', help='show debug', default=False, action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.root.setLevel(logging.DEBUG)

    if args.action == 'search':
        try:
            manager.Manager.get_instance().search(ip=args.address, callback=print_device)
        except error.Timeout:
            pass
        except error.KonkeError as err:
            print(err)
    else:
        try:
            if args.address is None:
                print('IP address is empty.')
                return

            if args.device == 'k2':
                device = K2(args.address)
            elif args.device == 'minik':
                device = MiniK(args.address)
            elif args.device == 'micmul':
                device = MicMul(args.address)
            elif args.device == 'mul':
                device = Mul(args.address)
            elif args.device == 'klight':
                device = KLight(args.address)
            elif args.device == 'kbulb':
                device = KBlub(args.address)
            else:
                raise error.IllegalDevice('device %s not support' % args.device)

            res = device.do(args.action, args.value)

            print(res if res else 'success')

        except error.KonkeError as err:
            print(err)

    exit(0)


if __name__ == "__main__":
    main()
