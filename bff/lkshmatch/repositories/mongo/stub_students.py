from lkshmatch.adapters.base import Player
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository

DATABASE_NAME = "match"


class MongoLKSHStudentsRepository(LKSHStudentsRepository):
    async def validate_register_user(self, user: Player) -> str:
        return "Egor"
