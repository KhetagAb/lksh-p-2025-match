from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, NewType

from lkshmatch.config import settings

PlayerId = NewType("PlayerId", int)
TeamId = NewType("TeamId", int)
SportSectionId = NewType("SportSectionId", int)
SportSectionName = NewType("SportSectionName", str)

API_URL = "http://" + str(settings.CORE_HOST) + ":" + str(settings.CORE_PORT)


class PlayerNotFound(Exception):
    pass


class PlayerAlreadyRegister(Exception):
    pass


class TeamIsFull(Exception):
    pass


class NameTeamReserveError(Exception):
    pass


class PlayerAlreadyInTeam(Exception):
    pass


class TeamNotFound(Exception):
    pass


class UnknownError(Exception):
    pass


class InsufficientRights(Exception):
    pass


CoreID = int


@dataclass
class Player:
    tg_username: str
    tg_id: int


@dataclass
class CorePlayer(Player):
    core_id: int


@dataclass
class PlayerToRegister(Player):
    name: str


@dataclass
class SportSection:
    name: str


@dataclass
class Team:
    name: str
    id: int
    name_sport_section: str
    capitan_id: int


@dataclass
class TournamentInterval:
    registration_deadline : int
    start: int
    end: int



@dataclass
class Tournament:
    id: int
    sport_name: SportSectionName


@dataclass
class Admin:
    tg_id: int


class PlayerAdapter(ABC):
    @abstractmethod
    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        raise NotImplementedError

    @abstractmethod
    async def register_user(self, user: PlayerToRegister) -> CoreID:
        raise NotImplementedError

    @abstractmethod
    async def get_player_id(self, user: Player) -> CoreID:
        raise NotImplementedError


class SportAdapter(ABC):
    @abstractmethod
    async def get_sections(self) -> List[SportSection]:
        raise NotImplementedError

    @abstractmethod
    async def get_players_by_sport_sections(self, section: SportSection) -> List[CorePlayer]:
        raise NotImplementedError

    @abstractmethod
    async def register_player_in_sport_section(self, section: SportSection, user: CorePlayer) -> None:
        raise NotImplementedError

    #@abstractmethod
    #async def get_all_sections(self): -> List[SportSection[List[CorePlayer]]]:
    #    raise NotImplementedError

class TournamentAdminAdapter(ABC):
    @abstractmethod
    async def create_tournament(
            self, tournament_interval: TournamentInterval, sport_name: SportSectionName, player_info: Admin
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_tournament(self, tournament: Tournament, player_info: Admin) -> None:
        raise NotImplementedError

    @abstractmethod
    async def modify_tournament(self, tournament: Tournament, player_info: Admin) -> None:
        raise NotImplementedError


class TournamentAdapter(ABC):
    @abstractmethod
    async def get_all_list_tournament(self) -> list[Tournament]:
        raise NotImplementedError

    @abstractmethod
    async def get_list_tournament(self, sport_name: SportSectionName) -> list[Tournament]:
        raise NotImplementedError

    @abstractmethod
    async def register_team_in_tournament(self, tournament: Tournament, team_id: TeamId, player_info: Player) -> None:
        raise NotImplementedError

    @abstractmethod
    async def unregister_team_in_tournament(self, tournament: Tournament, team_id: TeamId, player_info: Player) -> None:
        raise NotImplementedError


class TeamAdapter(ABC):
    @abstractmethod
    async def create_team(self, section: SportSection, user: Player, name_team: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def teams(self, section: SportSection) -> list[Team]:
        raise NotImplementedError

    @abstractmethod
    async def join_team(self, team: Team, user: Player) -> int:
        raise NotImplementedError

    @abstractmethod
    async def leave_team(self, team: Team, user: Player) -> None:
        raise NotImplementedError

    @abstractmethod
    async def approve(self, team: Team, user: Player):
        raise NotImplementedError
