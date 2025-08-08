import hashlib
import os
import json

JWT_SECRET_KEY = "hahaha"
BOT_TOKEN_HASH = hashlib.sha256(os.environ["BOT_TOKEN"].encode())
COOKIE_NAME = 'auth-token'
ALGORITHM = "HS256"