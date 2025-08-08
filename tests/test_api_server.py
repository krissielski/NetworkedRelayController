import pytest
from src.api_server import app, init_api
from src.relay_controller import RelayController
from src.config_manager import ConfigManager
from src.logger import setup_logger

class MockRelayController:
    def __init__(self):
        self.status = {1: False, 2: False, 3: False, 4: False}
    def turn_on(self, relay_id): self.status[relay_id] = True
    def turn_off(self, relay_id): self.status[relay_id] = False
    def turn_all_on(self):
        for rid in self.status: self.status[rid] = True
    def turn_all_off(self):
        for rid in self.status: self.status[rid] = False
    def get_status(self):
        return [{"id": rid, "state": "ON" if self.status[rid] else "OFF"} for rid in self.status]

@pytest.fixture
def client(tmp_path):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text("""
api:
  host: "0.0.0.0"
  port: 5000
relays:
  pins:
    1: 31
    2: 33
    3: 35
    4: 37
logging:
  level: "INFO"
  file: "test.log"
system:
  version: "1.0.0"
""")
    config = ConfigManager(str(config_path))
    logger = setup_logger("TestAPI", "DEBUG")
    relay_ctrl = MockRelayController()
    test_app = init_api(relay_ctrl, config, logger)
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        yield client

def test_relay_all_on(client):
    resp = client.post("/relay/all/on")
    assert resp.status_code == 200
    assert resp.json["status"] == "success"

def test_relay_all_off(client):
    resp = client.post("/relay/all/off")
    assert resp.status_code == 200
    assert resp.json["status"] == "success"

def test_relay_on_off(client):
    resp = client.post("/relay/1/on")
    assert resp.status_code == 200
    assert resp.json["relay"] == 1
    resp = client.post("/relay/1/off")
    assert resp.status_code == 200
    assert resp.json["relay"] == 1

def test_status(client):
    resp = client.get("/relay/status")
    assert resp.status_code == 200
    assert "relays" in resp.json

def test_version(client):
    resp = client.get("/system/version")
    assert resp.status_code == 200
    assert "version" in resp.json

def test_health(client):
    resp = client.get("/system/health")
    assert resp.status_code == 200
    assert resp.json["status"] == "healthy"
