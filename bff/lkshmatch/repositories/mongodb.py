from pymongo import MongoClient
from lkshmatch.config import settings

MONGO_URL = "mongodb://mongodb:mongodb@localhost:27017/mongodb"

def create_mongodb_client():
    return MongoClient(MONGO_URL)
