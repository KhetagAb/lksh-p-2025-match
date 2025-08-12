from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Player:
    tg_username: str
    name: str


class PlayerRepository(ABC):
    @abstractmethod
    def get_players(self) -> list[Player]:
        raise NotImplementedError
