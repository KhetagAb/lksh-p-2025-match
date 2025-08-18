import hashlib

from lkshmatch.domain.repositories.admin_repository import AdminRepository


class PrivilegeChecker:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def check_admin(self, creator_id: int) -> dict[str, str]:
        admins_list = self.admin_repository.get_admins()
        headers = {"admin_token": " "}
        for admin in admins_list:
            if admin == creator_id:
                mb5_hash_tg_id = hashlib.md5(str(creator_id).encode()).hexdigest()
                headers["admin_token"] = mb5_hash_tg_id
        return headers
