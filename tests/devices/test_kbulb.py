import pytest
from mock.mock_kbulb import MockKBulb
from pykonkeio.device.kbulb import KBulb
from pykonkeio import manager as client_manager


@pytest.fixture(scope='module')
def server(device_address, request):
    if not device_address:
        mock_server = MockKBulb()
        request.addfinalizer(lambda: mock_server.stop())
        return mock_server


@pytest.fixture(scope='module')
def client(device_address):
    client_manager.clear_device_info()
    return KBulb(device_address or '127.0.0.1')


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on(server: MockKBulb, client: KBulb):
    if server:
        server.start()

    await client.turn_on()
    assert client.status == 'open'
    if server:
        assert server.status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off(server: MockKBulb, client: KBulb):
    if server:
        server.start()

    await client.turn_off()
    assert client.status == 'close'
    if server:
        assert server.status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_set_brightness(server: MockKBulb, client: KBulb):
    if server:
        server.start()

    await client.turn_on()

    for i in range(10, 100, 10):
        await client.set_brightness(i)

        assert int(client.brightness) == i
        if server:
            assert int(server.brightness) == i


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_set_ct(server: MockKBulb, client: KBulb):
    if server:
        server.start()

    await client.turn_on()
    for i in range(2700, 6500, 500):
        await client.set_ct(i)

        assert int(client.ct) == i
        if server:
            assert int(server.ct) == i


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_update(server: MockKBulb, client: KBulb):
    if server:
        server.start()
        server.status = 'close'
        await client.update()
        assert client.status == server.status

        server.status = 'open'
        server.ct = 2700
        server.brightness = 10
        await client.update()
        assert client.status == server.status
        assert client.ct == server.ct
        assert client.brightness == server.brightness

        server.ct = 6500
        server.brightness = 100
        await client.update()
        assert client.ct == server.ct
        assert client.brightness == server.brightness

        server.status = 'close'
        await client.update()
        assert client.status == server.status

    else:
        await client.turn_off()
        await client.update()
        assert client.status == 'close'

        await client.turn_on()
        await client.set_brightness(10)
        await client.set_ct(2700)
        await client.update()
        assert client.status == 'open'
        assert client.ct == 2700
        assert client.brightness == 10

        await client.set_brightness(100)
        await client.set_ct(6500)
        await client.update()
        assert client.status == 'open'
        assert client.ct == 6500
        assert client.brightness == 100

        await client.turn_off()
        await client.update()
        assert client.status == 'close'
