import pytest
import re
from ..mock.mock_k2 import MockK2
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
    if not server:
        return

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
