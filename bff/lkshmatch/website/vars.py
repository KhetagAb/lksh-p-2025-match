import hashlib
import os
from lkshmatch.config import settings

# Telegram auth
JWT_SECRET_KEY = settings.get("WEBSITE_JWT_SECRET_KEY")
BOT_TOKEN_HASH = hashlib.sha256(settings.get("TELEGRAM_TOKEN").encode())
COOKIE_NAME = "auth-token"
ALGORITHM = "HS256"

# Google sheets
CREDENTIALS_FILE = settings.get("WEBSITE_CREDENTIALS_FILE")  # имя файла с закрытым ключом для google-таблиц
SERVICE_ACCOUNT_NAME = settings.get("WEBSITE_SERVICE_ACCOUNT_NAME")  # почта сервисного аккаунта
WEBSITE_IP = settings.get("WEBSITE_IP")
WEBSITE_PORT = settings.get("WEBSITE_PORT")