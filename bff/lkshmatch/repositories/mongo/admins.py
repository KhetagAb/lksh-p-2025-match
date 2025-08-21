from pymongo import MongoClient

from lkshmatch.domain.repositories.admin_repository import Admin, AdminRepository

DATABASE_NAME = "match"


class MongoAdminRepository(AdminRepository):
    def __init__(self, mongo_client: MongoClient):
        self.client: MongoClient = mongo_client

    def get_admins(self) -> list[dict]:
        return list(self.client[DATABASE_NAME]["students"].find({'parallel' : 'admin'}))

