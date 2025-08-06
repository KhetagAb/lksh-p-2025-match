from abc import ABC, abstractmethod
from dataclasses import dataclass
from os.path import extsep
from typing import NewType

PlayerId = NewType("PlayerId", int)
SportSectionId = NewType("SectionId", int)

class PlayerNotFound(Exception):
    pass

class AnotherError(Exception):
    pass

@dataclass
class PlayerAddInfo:
    tg_username: str
    tg_id: int

@dataclass
class PlayerRegisterInfo:
    name: str
    id: int

@dataclass
class SportSection:
    id: SportSectionId
    name: str


@dataclass
class Player:
    name: str
    is_coach: bool


class ValidateRegisterUser(ABC):
    @abstractmethod
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        raise NotImplementedError

class RegisterUser(ABC):
    @abstractmethod
    async def register_user(self, user: PlayerAddInfo) -> (str, PlayerId):
        raise NotImplementedError


class GetSportSections(ABC):
    @abstractmethod
    async def get_sections(self) -> list[SportSection]:
        raise NotImplementedError


class GetPlayersBySportSections(ABC):
    @abstractmethod
    async def players_by_sport_sections(self, section_id: SportSectionId) -> list[Player]:
        raise NotImplementedError

class RegisterPlayerInSection(ABC):
    @abstractmethod
    async def register_player_in_sectoin(self, user: PlayerAddInfo, section_id: SportSectionId) -> str:
        raise NotImplementedError