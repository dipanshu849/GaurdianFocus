import logging
import os

def get_logger(name):
    logger = logging.getLogger(name)

    level  = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(level)
    
    if logger.hasHandlers():
        return logger

    ch = logging.StreamHandler()
    ch.setLevel(level)

    fmt = logging.Formatter(
      "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger