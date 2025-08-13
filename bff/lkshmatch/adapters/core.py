from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NewType
from config import settings

PlayerId = NewType("PlayerId", int)
TeamId = NewType("TeamId", int)
SportSectionId = NewType("SportSectionId", int)
SportSectionName = NewType("SportSectionName", str)

API_URL = str(settings.CORE_HOST) + ':' + str(settings.CORE_PORT)


class PlayerNotFound(Exception):
    pass


class TeamIsFull(Exception):
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


@dataclass
class TournamentInterval:
    start: int
    end: int


@dataclass
class Tournament:
    id: int
    sport_name: SportSectionName


class ValidateRegisterPlayer(ABC):
    @abstractmethod
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        raise NotImplementedError


class RegisterPlayer(ABC):
    @abstractmethod
    async def register_user(self, user: PlayerAddInfo) -> PlayerRegisterInfo:
        raise NotImplementedError


class GetSportSections(ABC):
    @abstractmethod
    async def get_sections(self) -> list[SportSection]:
        raise NotImplementedError


class GetPlayersBySportSections(ABC):
    @abstractmethod
    async def get_players_by_sport_sections(self, section_id: SportSection) -> list[PlayerRegisterInfo]:
        raise NotImplementedError


class RegisterPlayerInSpotrSection(ABC):
    @abstractmethod
    async def register_player_in_sport_section(self, section: SportSection, user: PlayerRegisterInfo) -> None:
        raise NotImplementedError


class CreateTournament(ABC):
    @abstractmethod
    async def create_tournament(self, tournament_interval: TournamentInterval, sport_name: SportSectionName) -> None:
        raise NotImplementedError


class GetAllListTournament(ABC):
    @abstractmethod
    async def get_all_list_tournament(self) -> list[Tournament]:
        raise NotImplementedError


class GetListTournament(ABC):
    @abstractmethod
    async def get_list_tournament(self, sport_name: SportSectionName) -> list[Tournament]:
        raise NotImplementedError


class RegisterTeamInTournament(ABC):
    @abstractmethod
    async def register_team_in_tournament(self, tournament: Tournament, team_id: TeamId) -> None:
        raise NotImplementedError


class UnregisterTeamInTournament(ABC):
    @abstractmethod
    async def unregister_team_in_tournament(self, tournament: Tournament, team_id: TeamId) -> None:
        raise NotImplementedError

class RemoveTournament(ABC):
    @abstractmethod
    async def remove_tournament(self, tournament: Tournament) -> None:
        raise NotImplementedError


class ModifyTournament(ABC):
    @abstractmethod
    async def modify_tournament(self, tournament: Tournament) -> None:
        raise NotImplementedError
