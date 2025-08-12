from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# bad, but i'm pissed off, smb fix it
from lkshmatch.adapters.base import Player


@dataclass
class Student:
    tg_username: str
    name: str


class LKSHStudentsRepository(ABC):
    @abstractmethod
    async def get_players(self) -> List[Student]:
        raise NotImplementedError

    @abstractmethod
    async def validate_register_user(self, user: Player) -> str:
        raise NotImplementedError
