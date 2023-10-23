import logging
from config import logger as config_logger

logger = logging.getLogger(__name__)
logger.setLevel(config_logger.LOG_LEVEL)

# Create a formatter
formatter = logging.Formatter(config_logger.LOG_FORMAT)

# Create a console handler and set the level
console_handler = logging.StreamHandler()
console_handler.setLevel(config_logger.LOG_LEVEL)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)


def log(app_name, level, message):
    log_message = f"[{app_name}] {message}"
    if level in logging._nameToLevel:
        logger.log(logging._nameToLevel[level], log_message)
        print(log_message)
    else:
        raise ValueError("Invalid log level")