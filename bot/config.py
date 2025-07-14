import os

# 預設值，可用環境變數覆蓋
IB_HOST = os.getenv("IB_HOST", "127.0.0.1")
IB_PORT = int(os.getenv("IB_PORT", 4002))
IB_CLIENT_ID = int(os.getenv("IB_CLIENT_ID", 1))