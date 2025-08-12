from pymongo import MongoClient

from lkshmatch.adapters.base import Player, PlayerNotFound
from lkshmatch.domain.repositories.player_repository import LKSHStudentsRepository, Student

DATABASE_NAME = "match"


class MongoLKSHStudentsRepository(LKSHStudentsRepository):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    async def get_players(self) -> list[Student]:
        return list(self.mongo_client[DATABASE_NAME]["players"].find())

    async def validate_register_user(self, user: Player) -> str:
        players = await self.get_players()
        ans = ""
        for i in players:
            if i.tg_username == user.tg_username:
                ans = i.name
        if ans == "":
            raise PlayerNotFound

        return ans
