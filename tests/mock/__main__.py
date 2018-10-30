import asyncio
import logging
import sys
sys.path.append('/Users/jedmeng/Code/Toys/python/python-konkeio/')


if __name__ == "__main__":
    from .mock_k1 import MockK1
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(message)s')
    MockK1()
    loop = asyncio.get_event_loop()
    loop.run_forever()
