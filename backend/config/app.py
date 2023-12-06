import os
import dotenv

dotenv.load_dotenv()

INVITE_KEY = os.environ.get("INVITE_KEY")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
IS_DEBUG = os.environ.get("IS_DEBUG", 'TRUE') == 'TRUE'
DEEP_TRANSACTIONS_SCAN_DEPTH_IN_DAYS = 365
SHALLOW_TRANSACTION_SCAN_DEPTH_IN_DAYS = 30
STOP_AT_FAILED_LOGIN_THRESHOLD = 5
MAX_TRANSACTIONS_PER_REQUEST = 1000
TRANSACTIONS_CHUNK_SIZE = 50