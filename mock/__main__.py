import asyncio
import logging
import argparse
import sys


def main(event_loop):
    parser = argparse.ArgumentParser(prog="konkeio")
    parser.add_argument('device', help='device type')

    args = parser.parse_args()
    device_type = args.device.lower()

    if device_type == 'k1':
        from .mock_k1 import MockK1
        device = MockK1()
    elif device_type == 'k2':
        from .mock_k2 import MockK2
        device = MockK2()
    elif device_type == 'minik':
        from .mock_minik import MockMiniK
        device = MockMiniK()
    elif device_type == 'kbulb':
        from .mock_kbulb import MockKBulb
        device = MockKBulb()
    elif device_type == 'klight':
        from .mock_klight import MockKLight
        device = MockKLight()
    elif device_type == 'micmul':
        from .mock_micmul import MockMicMul
        device = MockMicMul()
    elif device_type == 'mul':
        from .mock_mul import MockMul
        device = MockMul()
    else:
        logging.error('Device not support: %s', device_type)
        return False

    device.start(event_loop)
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(message)s')
    loop = asyncio.get_event_loop()

    if not main(loop):
        sys.exit(0)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
