from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class Student:
    tg_username: str
    name: str


class LKSHStudentsRepository(ABC):
    @abstractmethod
    async def get_name_by_username(self, tg_username: str) -> str:
        raise NotImplementedError
