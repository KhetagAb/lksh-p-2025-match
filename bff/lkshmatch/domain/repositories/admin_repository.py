from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Admin:
    tg_id: int


class AdminRepository(ABC):
    @abstractmethod
    def get_admins(self) -> List[Admin]:
        raise NotImplementedError
