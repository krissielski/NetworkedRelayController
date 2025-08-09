import logging
import os
from typing import Optional

def setup_logger(name: str, level: str = "INFO", log_file: Optional[str] = None, console: bool = True) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s]: %(message)s')

    # Console handler (optional)
    if console:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # File handler
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
