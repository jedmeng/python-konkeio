import pytest
import re


def pytest_addoption(parser):
    parser.addoption("--device", help="device type")
    parser.addoption("--ip", help="device address")


@pytest.fixture(scope='session')
def device_address(request):
    if request.config.getoption("--device"):
        return request.config.getoption("--ip")

def pytest_collection_modifyitems(config, items):
    device = config.getoption("--device") 
    if not device or not config.getoption("--ip"):
        return
    
    skip = pytest.mark.skip(reason="device not match")
    for item in items:
        if item.parent.name[5:-3] != device:
            item.add_marker(skip)


