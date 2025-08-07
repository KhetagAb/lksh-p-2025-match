import hashlib
import os
import json

with open('.env', "r", encoding="utf-8") as file:
    data = json.load(file)

JWT_SECRET_KEY = "hahaha"
BOT_TOKEN_HASH = hashlib.sha256(data['BOT_TOKEN'].encode())
COOKIE_NAME = 'auth-token'
WHITELIST = [] #[ "671749585" ]
ALGORITHM = "HS256"