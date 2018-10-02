import argparse
import logging
from . import manager
from . import *

logging.basicConfig(level=logging.WARN,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s %(levelname)s %(message)s')


def print_device(ip, mac, password, action, device_type):
    print('ip: %s\nmac: %s\npassword: %s\n\n' % (ip, mac, password))


def main():
    example = '''
example:
konkeio search                              # search device
konkeio -a 192.168.0.255 search             # search device
konkeio -a 192.168.0.200 -d switch turn_on      # turn on switch
konkeio -a 192.168.0.200 turn_on                # turn on switch (switch is default device)
konkeio -a 192.168.0.200 turn_off               # turn off switch
konkeio -a 192.168.0.200 turn_on_night_light    # turn on night light (k2 only)
konkeio -a 192.168.0.200 turn_off_night_light   # turn off night light (k2 only)
konkeio -a 192.168.0.200 -d klight turn_on          # turn on klight
konkeio -a 192.168.0.200 -d klight turn_off         # turn off klight
konkeio -a 192.168.0.200 -d klight set_brightness 100       # set brightness of klight 
konkeio -a 192.168.0.200 -d klight set_color 128,128,128    # set color of klight
'''
    parser = argparse.ArgumentParser(prog="konkeio", epilog=example,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', dest='device', help='switch, klight, kblum', default='switch')
    parser.add_argument('-a', dest='address', help='device ip address', default='255.255.255.255')
    parser.add_argument('-v', dest='verbose', help='show debug', default=False, action="store_true")
    parser.add_argument('action', help='open, close, check or search')
    parser.add_argument('value', help='action value', nargs='?')

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

            if args.device == 'switch':
                device = Switch(args.address)
            elif args.device == 'klight':
                device = KLight(args.address)
            elif args.device == 'kbulb':
                device = KBlub(args.address)
            else:
                print('device %s not support' % args.device)
                return

            if args.action == 'check' and args.device == 'klight':
                [r, g, b] = device.color
                print('status: %s' % device.status)
                print('color: %d %d %d' % (r, g, b))
                print('brightness: %d' % device.brightness)

            elif args.action == 'check' and args.device == 'kbulb':
                print('status: %s' % device.status)

            elif args.action == 'check':
                print('status: %s' % device.status)

            elif args.action == 'open' or args.action == 'turn_on':
                if device.turn_on():
                    print('Turn on success')
                else:
                    print('Turn on failed')

            elif args.action == 'close' or args.action == 'turn_off':
                if device.turn_off():
                    print('Turn off success')
                else:
                    print('Turn off failed')

            elif args.action == 'turn_on_night_light':
                device.turn_on_light()
                print('Turn on night light success')

            elif args.action == 'turn_off_night_light':
                device.turn_off_light()
                print('Turn off night light success')

            elif args.action == 'set_brightness' and args.device == 'klight':
                device.set_brightness(args.value)
                print('Set brightness success')
            elif args.action == 'set_color' and args.device == 'klight':
                device.set_color(*args.value.split(','))
                print('Set color success')

            else:
                print('action is illegal.')

        except error.KonkeError as err:
            print(err)

    exit(0)


if __name__ == "__main__":
    main()
