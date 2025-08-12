from typing import List
from pymongo import MongoClient
from lkshmatch.domain.repositories.admin_repository import AdminRepository, Admin

DATABASE_NAME = "match"

class MongoAdminRepository(AdminRepository):
    def __init__(self, mongo_client: MongoClient):
        self.client: MongoClient = mongo_client

    def get_admins(self) -> List[Admin]:
        return list(self.client[DATABASE_NAME]['admins'].find())
