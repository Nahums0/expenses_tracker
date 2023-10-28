import os

INVITE_KEY = os.environ.get("INVITE_KEY")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
IS_DEBUG = os.environ.get("IS_DEBUG", 'TRUE') == 'TRUE'
DEEP_TRANSACTIONS_SCAN_DEPTH_IN_DAYS = 365