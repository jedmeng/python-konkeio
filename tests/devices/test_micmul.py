import pytest
import random
from ..mock.mock_micmul import MockMicMul
from pykonkeio.device.micmul import MicMul
from pykonkeio import manager as client_manager


@pytest.fixture(scope='module')
def server(device_address, request):
    if not device_address:
        mock_server = MockMicMul()
        request.addfinalizer(lambda: mock_server.stop())
        return mock_server


@pytest.fixture(scope='module')
def client(device_address):
    client_manager.clear_device_info()
    return MicMul(device_address or '127.0.0.1')


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on(server: MockMicMul, client: MicMul):
    if server:
        server.start()

    for i in range(client.socket_count):
        await client.turn_on(i)
        assert client.status[i] == 'open'
        if server:
            assert server.status[i] == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off(server: MockMicMul, client: MicMul):
    if server:
        server.start()

    for i in range(client.socket_count):
        await client.turn_off(i)
        assert client.status[i] == 'close'
        if server:
            assert server.status[i] == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on_all(server: MockMicMul, client: MicMul):
    if server:
        server.start()

    await client.turn_on_all()
    for i in range(client.socket_count):
        assert client.status[i] == 'open'
        if server:
            assert server.status[i] == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off_all(server: MockMicMul, client: MicMul):
    if server:
        server.start()

    await client.turn_off_all()
    for i in range(client.socket_count):
        assert client.status[i] == 'close'
        if server:
            assert server.status[i] == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_update(server: MockMicMul, client: MicMul):
    if not server:
        return

    server.start()
    server.status = list(['close'] * client.socket_count)
    await client.update()
    assert client.status == server.status

    server.status = list(['open'] * client.socket_count)
    await client.update()
    assert client.status == server.status

    server.status = list(['close'] * client.socket_count)
    await client.update()
    assert client.status == server.status

    server.status = list(random.choice(('open', 'close')) for _ in client.status)
    print(server.status)
    await client.update()
    assert client.status == server.status
