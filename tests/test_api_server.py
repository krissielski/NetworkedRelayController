def make_config_file():
        config_text = """
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
"""
        import tempfile
        tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml')
        tmp.write(config_text)
        tmp.close()
        return tmp.name


import unittest
import tempfile
import os
from src.api_server import init_api
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

class ApiServerTestCase(unittest.TestCase):
    def setUp(self):
        config_path = make_config_file()
        self.config_path = config_path
        config = ConfigManager(config_path)
        logger = setup_logger("TestAPI", "DEBUG")
        relay_ctrl = MockRelayController()
        self.app = init_api(relay_ctrl, config, logger)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_relay_on_off(self):
        resp = self.client.post("/relay/1/on")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["relay"], 1)
        resp = self.client.post("/relay/1/off")
        self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()

