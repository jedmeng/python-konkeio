import time
import pytest
from mock.mock_minik import MockMiniK
from pykonkeio.device.minik import MiniK
from pykonkeio import manager as client_manager


@pytest.fixture(scope='module')
def server(device_address, request):
    if not device_address:
        mock_server = MockMiniK()
        request.addfinalizer(lambda: mock_server.stop())
        return mock_server


@pytest.fixture(scope='module')
def client(device_address):
    client_manager.clear_device_info()
    return MiniK(device_address or '127.0.0.1')


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_on(server: MockMiniK, client: MiniK):
    if server:
        server.start()

    await client.turn_on()
    assert client.status == 'open'
    if server:
        assert server.status == 'open'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_turn_off(server: MockMiniK, client: MiniK):
    if server:
        server.start()

    await client.turn_off()
    assert client.status == 'close'
    if server:
        assert server.status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_update(server: MockMiniK, client: MiniK):
    if server:
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

    else:
        await client.turn_off()
        await client.update()
        assert client.status == 'close'

        await client.turn_on()
        await client.update()
        assert client.status == 'open'

        await client.turn_off()
        await client.update()
        assert client.status == 'close'


# noinspection 801,PyShadowingNames
@pytest.mark.asyncio
async def test_ir(server: MockMiniK, client: MiniK):
    if server:
        server.start()

    await client.update()

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
            await client.ir_learn(test_ir_id1, test_group, 10)
            assert time.time() - start <= 15

        await client.ir_quit()
        await client.ir_emit(test_ir_id1, test_group)
        await client.ir_remove(test_ir_id1, test_group)
        await client.ir_remove_group(test_group)
