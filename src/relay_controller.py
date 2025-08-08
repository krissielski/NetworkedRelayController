from typing import List, Dict
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for non-RPi environments
    class GPIO:
        BCM = BOARD = OUT = None
        @staticmethod
        def setmode(mode): pass
        @staticmethod
        def setup(pin, mode): pass
        @staticmethod
        def output(pin, state): pass
        @staticmethod
        def cleanup(): pass

class RelayController:
    def __init__(self, pin_map: Dict[int, int], logger):
        self.pin_map = pin_map
        self.logger = logger
        self.status = {rid: False for rid in pin_map}
        GPIO.setmode(GPIO.BOARD)
        for rid, pin in pin_map.items():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def turn_on(self, relay_id: int):
        self._validate_id(relay_id)
        pin = self.pin_map[relay_id]
        GPIO.output(pin, True)
        self.status[relay_id] = True
        self.logger.info(f"Relay {relay_id} ON")

    def turn_off(self, relay_id: int):
        self._validate_id(relay_id)
        pin = self.pin_map[relay_id]
        GPIO.output(pin, False)
        self.status[relay_id] = False
        self.logger.info(f"Relay {relay_id} OFF")

    def turn_all_on(self):
        for rid in self.pin_map:
            self.turn_on(rid)
        self.logger.info("All relays ON")

    def turn_all_off(self):
        for rid in self.pin_map:
            self.turn_off(rid)
        self.logger.info("All relays OFF")

    def get_status(self) -> List[Dict[str, str]]:
        return [{"id": rid, "state": "ON" if self.status[rid] else "OFF"} for rid in self.pin_map]

    def _validate_id(self, relay_id: int):
        if relay_id not in self.pin_map:
            self.logger.error(f"Invalid relay ID: {relay_id}")
            raise ValueError("Invalid relay ID")

    def cleanup(self):
        GPIO.cleanup()
        self.logger.info("GPIO cleanup done")
