import logging
from config import logger as config_logger

global logger
logger = None

def log(app_name, level, message):
    global logger
    if logger is None:
        logger = logging.getLogger("application_logger")
        logger.setLevel(config_logger.LOG_LEVEL)

        # Create a formatter
        formatter = logging.Formatter(config_logger.LOG_FORMAT)
        logger.handlers = []

        # Create a handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False


    log_message = f"[{app_name}] {message}"
    if level in logging._nameToLevel:
        logger.log(logging._nameToLevel[level], log_message)
    else:
        raise ValueError("Invalid log level")