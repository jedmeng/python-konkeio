import pytest
import re
import time
import asyncio
from mock.mock_k2 import MockK2
from pykonkeio.device.k2 import K2
from pykonkeio import manager as client_manager


@pytest.fixture(scope='module')
def server(device_address, request):
    if not device_address:
        mock_server = MockK2()
        request.addfinalizer(lambda: mock_server.stop())
        return mock_server


@pytest.fixture(scope='module')
def client(device_address):
    client_manager.clear_device_info()
    return K2(device_address or '127.0.0.1')


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_on()
    assert client.status == 'open'
    if server:
        assert server.status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_off()
    assert client.status == 'close'
    if server:
        assert server.status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on_light(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_on_light()
    assert client.light_status == 'open'
    if server:
        assert server.light_status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off_light(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_off_light()
    assert client.light_status == 'close'
    if server:
        assert server.light_status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on_usb(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_on_usb()
    assert client.usb_status == 'open'
    if server:
        assert server.usb_status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off_usb(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_off_usb()
    assert client.usb_status == 'close'
    if server:
        assert server.usb_status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_check_power(server: MockK2, client: K2):
    if server:
        server.start()

    await client.turn_on()
    client_power = await client.get_power()
    assert re.match(r'^\d+\.\d{2}$', client_power)
    if server:
        assert float(server.last_power) == float(client_power)


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_update(server: MockK2, client: K2):
    if server:
        server.start()
        server.status = 'close'
        server.usb_status = 'close'
        server.light_status = 'close'
        await client.update()
        assert client.status == server.status
        assert client.usb_status == server.usb_status
        assert client.light_status == server.light_status

        server.status = 'open'
        server.usb_status = 'open'
        server.light_status = 'open'
        await client.update()
        assert client.status == server.status
        assert client.usb_status == server.usb_status
        assert client.light_status == server.light_status

        server.status = 'close'
        server.usb_status = 'close'
        server.light_status = 'close'
        await client.update()
        assert client.status == server.status
        assert client.usb_status == server.usb_status
        assert client.light_status == server.light_status

    else:
        await client.turn_off()
        await client.turn_off_usb()
        await client.turn_off_light()
        await client.update()
        assert client.status == 'close'
        assert client.usb_status == 'close'
        assert client.light_status == 'close'

        await client.turn_on()
        await client.turn_on_usb()
        await client.turn_on_light()
        await client.update()
        assert client.status == 'open'
        assert client.usb_status == 'open'
        assert client.light_status == 'open'

        await client.turn_off()
        await client.turn_off_usb()
        await client.turn_off_light()
        await client.update()
        assert client.status == 'close'
        assert client.usb_status == 'close'
        assert client.light_status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_ir(server: MockK2, client: K2):
    if server:
        server.start()

    await client.update()

    if client.usb_status == 'close':
        await client.turn_on_usb()
        await asyncio.sleep(3)
        await client.fetch_info()

    if client.is_support_ir:
        test_group = 'test_group'
        test_ir_id = '1000'
        test_ir_id1 = '1001'
        if server:
            res = await client.ir_learn(test_ir_id, test_group)
            assert res is False
            res = await client.ir_learn(test_ir_id1)
            assert res is True
        else:
            start = time.time()
            await client.ir_learn(test_ir_id1, test_group)
            assert time.time() - start <= 35

        await client.ir_quit()
        await client.ir_emit(test_ir_id1, test_group)
        await client.ir_remove(test_ir_id1, test_group)
        await client.ir_remove_group(test_group)
        

# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_rf(server: MockK2, client: K2):
    if server:
        server.start()

    await client.update()

    if client.usb_status == 'close':
        await client.turn_on_usb()
        await asyncio.sleep(3)
        await client.fetch_info()

    if client.is_support_rf:
        test_group = 'test_group'
        test_rf_id = '1000'
        test_rf_id1 = '1001'
        if server:
            res = await client.rf_learn(test_rf_id, test_group)
            assert res is False
            res = await client.rf_learn(test_rf_id1)
            assert res is True
        else:
            start = time.time()
            await client.rf_learn(test_rf_id1, test_group)
            assert time.time() - start <= 35

        await client.rf_quit()
        await client.rf_emit(test_rf_id1, test_group)
        await client.rf_remove(test_rf_id1, test_group)
        await client.rf_remove_group(test_group)
