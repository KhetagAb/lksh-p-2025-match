from dataclasses import dataclass
from pymongo import MongoClient
from lkshmatch.domain.repositories.player_repository import PlayerRepository, Player
from lkshmatch.main import container

DATABASE_NAME = "match"

class MongoPlayerRepository(PlayerRepository):
    def __init__(self):
        with container() as app_scope:
            self.mongo_client: MongoClient = app_scope.get(MongoClient)

    def get_players(self) -> list[Player]:
        return list(self.mongo_client[DATABASE_NAME]['players'].find())
