from pymongo import MongoClient
from bff.lkshmatch.config import settings

API_URL = str(settings.CORE_HOST) + ':' + str(settings.CORE_PORT)


class CreateMongo():
    def __init__(self, host: API_URL):
        client = MongoClient()
