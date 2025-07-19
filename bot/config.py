import os
from dotenv import load_dotenv
from .logger_config import get_logger

logger = get_logger(__name__)

load_dotenv()

IB_HOST = os.environ.get("IB_HOST", "127.0.0.1")
IB_PORT = int(os.environ.get("IB_PORT", 4002))
IB_CLIENT_ID = int(os.environ.get("IB_CLIENT_ID", 1))
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_RECIPIENT = os.environ.get('MAILGUN_RECIPIENT')
NEED_AMOUMT = os.environ.get('NEED_AMOUMT', 5000)

logger.info(f"IB_HOST: {IB_HOST}")
logger.info(f"IB_PORT: {IB_PORT}")
logger.info(f"IB_CLIENT_ID: {IB_CLIENT_ID}")
logger.info(f"MAILGUN_API_KEY: {MAILGUN_API_KEY}")
logger.info(f"MAILGUN_DOMAIN: {MAILGUN_DOMAIN}")
logger.info(f"MAILGUN_RECIPIENT: {MAILGUN_RECIPIENT}")
logger.info(f"NEED_AMOUMT: {NEED_AMOUMT}")