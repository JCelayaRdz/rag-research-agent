import logging
import sys
from config import settings

LOG_FORMAT = "%(asctime)s [%(levelname)s %(name)s] - [%(funcname)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    
    logger.setLevel(settings.LOG_LEVEL_PARSED)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL_PARSED)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
