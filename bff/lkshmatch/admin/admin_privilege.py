import hashlib

from bff.lkshmatch.adapters.core import Admin
from bff.lkshmatch.repositories.admins import AdminsRepository


class PrivilegeChecker:
    def __init__(self, admin_repository: AdminsRepository):
        self.admin_repository = admin_repository

    def check_admin(self, player_info: Admin) -> dict[str, str]:
        admins_list = self.admin_repository.get_admins()
        headers = {'admin_token': " "}
        for admin in admins_list:
            if admin == player_info:
                mb5_hash_tg_id = hashlib.md5(str(player_info).encode()).hexdigest()
                headers['admin_token'] = mb5_hash_tg_id
        return headers
