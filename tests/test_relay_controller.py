import pytest
from src.relay_controller import RelayController

class MockLogger:
    def info(self, msg): pass
    def error(self, msg): pass

class MockGPIO:
    BOARD = OUT = None
    def setmode(self, mode): pass
    def setup(self, pin, mode): pass
    def output(self, pin, state): pass
    def cleanup(self): pass

@pytest.fixture
def relay_controller(monkeypatch):
    monkeypatch.setattr('src.relay_controller.GPIO', MockGPIO())
    pin_map = {1: 31, 2: 33, 3: 35, 4: 37}
    logger = MockLogger()
    return RelayController(pin_map, logger)

def test_turn_on_off(relay_controller):
    relay_controller.turn_on(1)
    assert relay_controller.status[1] is True
    relay_controller.turn_off(1)
    assert relay_controller.status[1] is False

def test_turn_all_on_off(relay_controller):
    relay_controller.turn_all_on()
    assert all(relay_controller.status.values())
    relay_controller.turn_all_off()
    assert not any(relay_controller.status.values())

def test_get_status(relay_controller):
    relay_controller.turn_on(2)
    status = relay_controller.get_status()
    assert status[1]['state'] == 'OFF'
    assert status[1]['id'] == 1
    assert status[2]['state'] == 'ON'
    assert status[2]['id'] == 2

def test_invalid_id(relay_controller):
    with pytest.raises(ValueError):
        relay_controller.turn_on(5)
