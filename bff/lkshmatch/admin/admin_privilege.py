import hashlib

from lkshmatch.adapters.base import Player
from lkshmatch.domain.repositories.admin_repository import AdminRepository
from lkshmatch.domain.repositories.admin_repository import Admin, AdminRepository


class PrivilegeChecker:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def check_admin(self, player_info: int) -> dict[str, str]:
        admins_list = self.admin_repository.get_admins()
        headers = {"admin_token": " "}
        for admin in admins_list:
            if admin == player_info:
                mb5_hash_tg_id = hashlib.md5(str(player_info).encode()).hexdigest()
                headers["admin_token"] = mb5_hash_tg_id
        return headers
