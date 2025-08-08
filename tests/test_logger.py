
import unittest
import logging
import tempfile
import os
from src.logger import setup_logger

class LoggerTestCase(unittest.TestCase):
    def test_logger_setup(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            log_file = os.path.join(tmpdirname, "test.log")
            logger = setup_logger("TestLogger", "DEBUG", log_file)
            logger.debug("debug message")
            logger.info("info message")
            logger.error("error message")
            with open(log_file) as f:
                content = f.read()
            self.assertIn("debug message", content)
            self.assertIn("info message", content)
            self.assertIn("error message", content)
            # Close and remove all handlers to release the file lock (Windows fix)
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)
            logging.shutdown()

if __name__ == "__main__":
    unittest.main()
