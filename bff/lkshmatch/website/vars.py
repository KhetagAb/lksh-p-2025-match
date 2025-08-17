import hashlib
import os

# Telegram auth
JWT_SECRET_KEY = os.getenv("WEBAPP_JWT_SECRET_KEY")
BOT_TOKEN_HASH = hashlib.sha256(os.getenv("TELEGRAM_TOKEN").encode())
COOKIE_NAME = "auth-token"
ALGORITHM = "HS256"

# Google sheets
CREDENTIALS_FILE = os.getenv("WEBAPP_CREDENTIALS_FILE")  # имя файла с закрытым ключом для google-таблиц
SERVICE_ACCOUNT_NAME = os.getenv("WEBAPP_SERVICE_ACCOUNT_NAME")  # почта сервисного аккаунта
