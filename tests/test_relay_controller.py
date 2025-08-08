
import unittest
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

class RelayControllerTestCase(unittest.TestCase):
    def setUp(self):
        # Patch GPIO in relay_controller module
        import src.relay_controller
        src.relay_controller.GPIO = MockGPIO()
        pin_map = {1: 31, 2: 33, 3: 35, 4: 37}
        logger = MockLogger()
        self.relay_controller = RelayController(pin_map, logger)

    def test_turn_on_off(self):
        self.relay_controller.turn_on(1)
        self.assertTrue(self.relay_controller.status[1])
        self.relay_controller.turn_off(1)
        self.assertFalse(self.relay_controller.status[1])

    def test_turn_all_on_off(self):
        self.relay_controller.turn_all_on()
        self.assertTrue(all(self.relay_controller.status.values()))
        self.relay_controller.turn_all_off()
        self.assertFalse(any(self.relay_controller.status.values()))

    def test_get_status(self):
        self.relay_controller.turn_on(2)
        status = self.relay_controller.get_status()
        self.assertEqual(status[0]['state'], 'OFF')
        self.assertEqual(status[0]['id'], 1)
        self.assertEqual(status[1]['state'], 'ON')
        self.assertEqual(status[1]['id'], 2)

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            self.relay_controller.turn_on(5)

if __name__ == "__main__":
    unittest.main()
