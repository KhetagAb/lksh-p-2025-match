import hashlib

from lkshmatch.domain.repositories.admin_repository import AdminRepository


class PrivilegeChecker:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def get_admin_token(self, requester_username: str) -> str:
        for admin in self.admin_repository.get_admins():
            if admin["tg_username"] == requester_username:
                return hashlib.md5(str(requester_username).encode()).hexdigest()
        return ""
