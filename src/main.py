import sys
import signal
from src.config_manager import ConfigManager
from src.logger import setup_logger
from src.relay_controller import RelayController
from src.api_server import init_api
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')


def graceful_shutdown(relay_controller, logger):
    def handler(signum, frame):
        logger.info("Shutting down...")
        relay_controller.cleanup()
        sys.exit(0)
    return handler


def main():
    # Load config
    config = ConfigManager(CONFIG_PATH)
    log_cfg = config.get('logging')
    logger = setup_logger('RelayController', log_cfg['level'], log_cfg['file'])

    # Relay controller
    pin_map = config.get('relays', 'pins')
    relay_controller = RelayController(pin_map, logger)

    # API server
    app = init_api(relay_controller, config, logger)

    # Handle signals
    signal.signal(signal.SIGINT, graceful_shutdown(relay_controller, logger))
    signal.signal(signal.SIGTERM, graceful_shutdown(relay_controller, logger))

    api_cfg = config.get('api')
    app.run(host=api_cfg['host'], port=api_cfg['port'])

if __name__ == "__main__":
    main()
