from dataclasses import dataclass
from pymongo import MongoClient

DATABASE_NAME = "match"

@dataclass
class Player:
    tg_username: str
    name: str

class PlayerRepositories:
    def __init__(self, mongoclient: MongoClient):
        self.client: MongoClient = mongoclient

    def get_player(self) -> list[Player]:
        return list(self.client[DATABASE_NAME]['players'].find())
