import logging
import os

LOG_FORMAT = os.environ.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_LEVEL = getattr(logging, os.environ.get('LOG_LEVEL', 'DEBUG').upper(), logging.DEBUG)
LOG_MAX_SIZE = int(os.environ.get('LOG_MAX_SIZE', str(1024 * 1024)))  # 1 MB
LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', '5'))
