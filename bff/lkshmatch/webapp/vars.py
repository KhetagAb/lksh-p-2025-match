import hashlib
import os

# Telegram auth
JWT_SECRET_KEY = "hahaha"
BOT_TOKEN_HASH = hashlib.sha256(os.environ["BOT_TOKEN"].encode())
COOKIE_NAME = 'auth-token'
ALGORITHM = "HS256"

# Google sheets
CREDENTIALS_FILE = '../test-project-468709-cdaea0b70d4c.json'  # имя файла с закрытым ключом для google-таблиц
SERVICE_ACCOUNT_NAME = 'test-646@test-project-468709.iam.gserviceaccount.com' # почта сервисного аккаунта