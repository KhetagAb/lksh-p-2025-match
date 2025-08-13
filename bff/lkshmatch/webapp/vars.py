import hashlib
import os
from config import settings

# Telegram auth
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
BOT_TOKEN_HASH = hashlib.sha256(os.environ['BOT_TOKEN'].encode())
ALGORITHM = settings.ALGORITHM
COOKIE_NAME = settings.COOKIE_NAME

# Google sheets
CREDENTIALS_FILE = os.environ['CREDENTIALS_FILE']  # имя файла с закрытым ключом для google-таблиц
SERVICE_ACCOUNT_NAME = os.environ['SERVICE_ACCOUNT_NAME'] # почта сервисного аккаунта
