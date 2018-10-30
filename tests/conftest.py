import pytest


def pytest_addoption(parser):
    parser.addoption("--device", help="device address")


@pytest.fixture(scope='session')
def device_address(request):
    return request.config.getoption("--device")
