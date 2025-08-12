from dataclasses import dataclass
from pymongo import MongoClient
from lkshmatch.domain.repositories.player_repository import PlayerRepository, Player

DATABASE_NAME = "match"

class MongoPlayerRepository(PlayerRepository):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    def get_players(self) -> list[Player]:
        return list(self.mongo_client[DATABASE_NAME]['players'].find())
