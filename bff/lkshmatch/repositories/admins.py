from dataclasses import dataclass
from typing import List

from pymongo import MongoClient

DATABASE_NAME = "match"

@dataclass
class Admin:
    tg_id: int

class AdminsRepository:
    def __init__(self, mongo_client: MongoClient):
        self.client: MongoClient = mongo_client

    def get_admins(self) -> List[Admin]:
        return list(self.client[DATABASE_NAME]['admins'].find())
