from pymongo import MongoClient

from lkshmatch.adapters.base import Player, PlayerNotFound, TgID
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository, Student

DATABASE_NAME = "match"


class MongoLKSHStudentsRepository(LKSHStudentsRepository):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    async def get_students(self) -> list[Student]:
        return list(self.mongo_client[DATABASE_NAME]["students"].find())

    async def get_name_by_username(self, tg_username: str) -> str:
        students = await self.get_students()
        for student in students:
            if student.tg_username == tg_username:
                return student.name
        raise PlayerNotFound
