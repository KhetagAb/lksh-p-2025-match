from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Admin:
    core_id: int


class AdminRepository(ABC):
    @abstractmethod
    def get_admins(self) -> list[Admin]:
        raise NotImplementedError
