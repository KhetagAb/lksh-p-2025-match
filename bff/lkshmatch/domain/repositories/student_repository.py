from abc import ABC, abstractmethod
from dataclasses import dataclass

# bad, but i'm pissed off, smb fix it
from lkshmatch.adapters.base import Player, TgID


@dataclass
class Student:
    tg_username: str
    name: str


class LKSHStudentsRepository(ABC):
    @abstractmethod
    async def get_students(self) -> list[Student]:
        raise NotImplementedError

    @abstractmethod
    async def get_name_by_username(self, tg_username: str) -> str:
        raise NotImplementedError
