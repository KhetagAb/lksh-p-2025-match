import hashlib
from typing import Optional

from lkshmatch.domain.repositories.admin_repository import AdminRepository


class PrivilegeChecker:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def get_admin_token(self, creator_id: int) -> Optional[str]:
        for admin in self.admin_repository.get_admins():
            if admin.core_id == creator_id:
                return hashlib.md5(str(creator_id).encode()).hexdigest()
        return None
