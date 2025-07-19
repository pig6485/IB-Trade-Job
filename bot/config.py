import os
from dotenv import load_dotenv

load_dotenv()

IB_HOST = os.environ.get("IB_HOST", "127.0.0.1")
IB_PORT = int(os.environ.get("IB_PORT", 4002))
IB_CLIENT_ID = int(os.environ.get("IB_CLIENT_ID", 1))
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_RECIPIENT = os.environ.get('MAILGUN_RECIPIENT')
NEED_AMOUMT = os.environ.get('NEED_AMOUMT', 5000)

print(f"IB_HOST: {IB_HOST}")
print(f"IB_PORT: {IB_PORT}")
print(f"IB_CLIENT_ID: {IB_CLIENT_ID}")
print(f"MAILGUN_API_KEY: {MAILGUN_API_KEY}")
print(f"MAILGUN_DOMAIN: {MAILGUN_DOMAIN}")
print(f"MAILGUN_RECIPIENT: {MAILGUN_RECIPIENT}")
print(f"NEED_AMOUMT: {NEED_AMOUMT}")