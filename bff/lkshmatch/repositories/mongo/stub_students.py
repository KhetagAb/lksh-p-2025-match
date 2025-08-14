from pymongo import MongoClient

from lkshmatch.adapters.base import Player, PlayerNotFound
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository, Student

DATABASE_NAME = "match"


class MongoLKSHStudentsRepository(LKSHStudentsRepository):
    async def validate_register_user(self, user: Player) -> str:
        return "Egor"
