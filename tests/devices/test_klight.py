import pytest
from mock.mock_klight import MockKLight
from pykonkeio.device.klight import KLight
from pykonkeio import manager as client_manager


@pytest.fixture(scope='module')
def server(device_address, request):
    if not device_address:
        mock_server = MockKLight()
        request.addfinalizer(lambda: mock_server.stop())
        return mock_server


@pytest.fixture(scope='module')
def client(device_address):
    client_manager.clear_device_info()
    return KLight(device_address or '127.0.0.1')


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on(server: MockKLight, client: KLight):
    if server:
        server.start()

    await client.turn_on()
    assert client.status == 'open'
    if server:
        assert server.status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off(server: MockKLight, client: KLight):
    if server:
        server.start()

    await client.turn_off()
    assert client.status == 'close'
    if server:
        assert server.status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_set_brightness(server: MockKLight, client: KLight):
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
async def test_set_color(server: MockKLight, client: KLight):
    if server:
        server.start()

    await client.turn_on()
    for i in [(0, 0, 0), (100, 100, 100), (255, 255, 255)]:
        await client.set_color(*i)

        assert tuple(int(c) for c in client.color) == i
        if server:
            assert tuple(int(c) for c in server.color) == i


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_update(server: MockKLight, client: KLight):
    if not server:
        return

    server.start()
    server.status = 'close'
    await client.update()
    assert client.status == server.status

    server.status = 'open'
    server.color = [100, 100, 100]
    server.brightness = 10
    await client.update()
    assert client.status == server.status
    assert client.color == server.color
    assert client.brightness == server.brightness

    server.color = [255, 255, 255]
    server.brightness = 100
    await client.update()
    assert client.color == server.color
    assert client.brightness == server.brightness

    server.status = 'close'
    await client.update()
    assert client.status == server.status
