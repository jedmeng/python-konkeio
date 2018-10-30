import argparse
import logging
import asyncio

from . import socket
from . import manager
from . import error

help_content = '''
usage: konkeio [action] [device] [address] [value] [--verbose]

Supported devices and actions supported by each device:
global: search help
k2:     get_status turn_[on/off] turn_[on/off]_usb turn_[on/off]_light
minik:  get_status turn_[on/off]
micmul: get_count get_status_all get_status[1/2/3/4] turn_[on/off]_all turn_[on/off]_socket[1/2/3/4]
mul:    get_count get_status_all get_status[1/2/3] get_usb_count get_usb_status_all get_usb_status[1/2] 
        turn_[on/off]_all turn_[on/off]_socket[1/2/3] turn_[on/off]_usb[1/2] 
klight: get_status get_brightness get_color turn_[on/off] set_brightness set_color
kbulb:  get_status get_brightness get_ct turn_[on/off] set_brightness set_ct

* each action starts with 'set_' must provide a value parameter

Value Format:
color:      r,g,b
ct:         2700-6500
brightness: 0-100

Example:
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
konkeio set_ct bulb 192.168.0.64 3400
konkeio turn_off bulb 192.168.0.64
'''


def print_device(ip, mac, password, *args):
    print('ip: %s\nmac: %s\npassword: %s\n\n' % (ip, mac, password))


async def main():
    parser = argparse.ArgumentParser(prog="konkeio", epilog=help_content,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', help='action name')
    parser.add_argument('device', help='device type', nargs='?')
    parser.add_argument('address', help='device ip address', nargs='?')
    parser.add_argument('value', help='action value', nargs='?')
    parser.add_argument('-v', dest='verbose', help='show debug', default=False, action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.root.setLevel(logging.DEBUG)

    if args.action == 'search':
        try:
            ip = args.device or '255.255.255.255'
            await manager.search(ip=ip, callback=print_device)
        except error.Timeout:
            pass
        except error.KonkeError as err:
            print(err)
    elif args.action == 'help':
        print(help_content)
    elif args.action == 'send':
        ip, mac, password, *_ = await manager.get_device_info(args.device)
        print(await socket.send_message((ip, mac, password, args.address, args.value)))
    else:
        try:
            if args.address is None or args.device is None:
                print('Usage: konkeio [action] [device] [address] [value] [--verbose]')
                print("Try 'konkeio help' for more information.")
                exit(0)

            device = manager.get_device(args.address, args.device)
            await device.update()
            res = await device.do(args.action, args.value)

            print(res if res else 'success')

        except error.KonkeError as err:
            print(err)

    current = asyncio.Task.current_task()
    for task in asyncio.Task.all_tasks():
        if task != current:
            task.cancel()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN,
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(message)s')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
