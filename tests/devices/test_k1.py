import pytest
from mock.mock_k1 import MockK1
from pykonkeio.device.k1 import K1
from pykonkeio import manager as client_manager


@pytest.fixture(scope='module')
def server(device_address, request):
    if not device_address:
        mock_server = MockK1()
        request.addfinalizer(lambda: mock_server.stop())
        return mock_server


@pytest.fixture(scope='module')
def client(device_address):
    client_manager.clear_device_info()
    return K1(device_address or '127.0.0.1')


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on(server: MockK1, client: K1):
    if server:
        server.start()

    await client.turn_on()
    assert client.status == 'open'
    if server:
        assert server.status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off(server: MockK1, client: K1):
    if server:
        server.start()

    await client.turn_off()
    assert client.status == 'close'
    if server:
        assert server.status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_update(server: MockK1, client: K1):
    if not server:
        return

    server.start()
    server.status = 'close'
    await client.update()
    assert client.status == server.status

    server.status = 'open'
    await client.update()
    assert client.status == server.status

    server.status = 'close'
    await client.update()
    assert client.status == server.status
