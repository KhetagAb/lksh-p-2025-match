from abc import ABC, abstractmethod
from dataclasses import dataclass
from os.path import extsep
from typing import NewType

PlayerId = NewType("PlayerId", int)

class PlayerNotFound(Exception):
    pass

class NameTeamReserveError(Exception):
    pass

class PlayerAlreadyInTeam(Exception):
    pass

class UnknownError(Exception):
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
    name: str
    en_name: str

@dataclass
class Team:
    name: str
    id: int
    name_sport_section: str
    capitan_id: int

class ValidateRegisterUser(ABC):
    @abstractmethod
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        raise NotImplementedError

class RegisterUser(ABC):
    @abstractmethod
    async def register_user(self, user: PlayerAddInfo) -> PlayerRegisterInfo:
        raise NotImplementedError


class GetSportSections(ABC):
    @abstractmethod
    async def get_sections(self) -> list[SportSection]:
        raise NotImplementedError


class GetPlayersBySportSections(ABC):
    @abstractmethod
    async def players_by_sport_sections(self, section_id: SportSection) -> list[PlayerRegisterInfo]:
        raise NotImplementedError

class RegisterPlayerInSportSection(ABC):
    async def register_player_in_sport_sectoin(self, section_id: SportSection, user_id: PlayerRegisterInfo) -> None:
        raise NotImplementedError



class CreateTeam(ABC):
    @abstractmethod
    async def create_team(self, section: SportSection, user: PlayerRegisterInfo, name_team: str) -> None:
        raise NotImplementedError

class GetTeams(ABC):
    @abstractmethod
    async def teams(self, section: SportSection) -> list[Team]:
        raise NotImplementedError

class JoinTeam(ABC):
    @abstractmethod
    async def join_team(self, team: Team, user: PlayerRegisterInfo) -> int:
        raise NotImplementedError

class LeaveTeam(ABC):
    @abstractmethod
    async def leave_team(self, team: Team, user: PlayerRegisterInfo) -> None:
        raise NotImplementedError

class Approve(ABC):
    @abstractmethod
    async def approve(self, team: Team, user: PlayerRegisterInfo):
        raise NotImplementedError