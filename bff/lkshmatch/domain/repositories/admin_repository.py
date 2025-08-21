from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Admin:
    requester_username: str


class AdminRepository(ABC):
    @abstractmethod
    def get_admins(self) -> list[dict]:
        raise NotImplementedError
