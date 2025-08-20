import hashlib

from lkshmatch.domain.repositories.admin_repository import AdminRepository


class PrivilegeChecker:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def get_admin_token(self, tg_username: str) -> str:
        admins = self.admin_repository.get_admins()
        for admin in admins:
            if admin["tg_username"] == tg_username:
                return hashlib.md5(tg_username.encode()).hexdigest()
        return ""
