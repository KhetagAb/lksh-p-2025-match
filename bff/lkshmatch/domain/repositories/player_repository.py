from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Student:
    tg_username: str
    name: str


class LKSHStudentsRepository(ABC):
    @abstractmethod
    def get_players(self) -> List[Student]:
        raise NotImplementedError
