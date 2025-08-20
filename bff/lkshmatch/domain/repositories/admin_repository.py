from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Admin:
    tg_username: str


class AdminRepository(ABC):
    @abstractmethod
    def get_admins(self) -> list[Admin]:
        raise NotImplementedError
