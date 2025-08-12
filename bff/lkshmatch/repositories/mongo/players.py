from typing import List

from pymongo import MongoClient

from lkshmatch.domain.repositories.player_repository import LKSHStudentsRepository, Student

DATABASE_NAME = "match"


class MongoLKSHStudentsRepository(LKSHStudentsRepository):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    def get_players(self) -> List[Student]:
        return list(self.mongo_client[DATABASE_NAME]["players"].find())
