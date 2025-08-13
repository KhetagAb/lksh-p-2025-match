from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, NewType

PlayerId = NewType("PlayerId", int)
TeamId = NewType("TeamId", int)
SportSectionId = NewType("SportSectionId", int)
SportSectionName = NewType("SportSectionName", str)


class PlayerNotFound(Exception):
    pass


class PlayerAlreadyRegister(Exception):
    pass


#
# class TeamIsFull(Exception):
#     pass
#
#
# class NameTeamReserveError(Exception):
#     pass
#
#
# class PlayerAlreadyInTeam(Exception):
#     pass
#
#
# class TeamNotFound(Exception):
#     pass
#
#
class UnknownError(Exception):
    pass


#
# class InsufficientRights(Exception):
#     pass
#
#
CoreID = int
TgID = int


@dataclass
class TeamMember:
    core_id: CoreID
    tg_id: TgID


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
    id: int
    name: str
    ru_name: str


@dataclass
class Activity:
    id: int
    sport_name: SportSectionName


@dataclass
class Team:
    id: int
    name: str
    capitan: TeamMember
    members: List[TeamMember]


# @dataclass
# class TournamentInterval:
#     registration_deadline: int
#     start: int
#     end: int
#
# @dataclass
# class Admin:
#     tg_id: int


class PlayerAdapter(ABC):
    @abstractmethod
    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        raise NotImplementedError

    @abstractmethod
    async def register_user(self, user: PlayerToRegister) -> CoreID:
        raise NotImplementedError


class SportAdapter(ABC):
    @abstractmethod
    async def get_all_sections(self) -> List[SportSection]:
        raise NotImplementedError


# class TournamentAdminAdapter(ABC):
#     @abstractmethod
#     async def create_tournament(
#         self, tournament_interval: TournamentInterval, sport_name: SportSectionName, player_info: Admin
#     ) -> None:
#         raise NotImplementedError
#
#     @abstractmethod
#     async def remove_tournament(self, activity: Activity, player_info: Admin) -> None:
#         raise NotImplementedError
#
#     @abstractmethod
#     async def modify_tournament(self, activity: Activity, player_info: Admin) -> None:
#         raise NotImplementedError


class ActivityAdapter(ABC):
    @abstractmethod
    async def get_activities_by_sport_section(self, sport_section_id: int) -> List[Activity]:
        raise NotImplementedError

    @abstractmethod
    async def get_activity_by_id(self, sport_section_id: int) -> List[Team]:
        raise NotImplementedError

    @abstractmethod
    async def make_team_in_activity(self, activity: Activity, team_id: TeamId, player_info: Player) -> None:
        raise NotImplementedError

# class TeamAdapter(ABC):
#     @abstractmethod
#     async def create_team(self, section: SportSection, user: Player, name_team: str) -> None:
#         raise NotImplementedError
#
#     @abstractmethod
#     async def teams(self, section: SportSection) -> list[Team]:
#         raise NotImplementedError
#
#     @abstractmethod
#     async def join_team(self, team: Team, user: Player) -> int:
#         raise NotImplementedError
#
#     @abstractmethod
#     async def leave_team(self, team: Team, user: Player) -> None:
#         raise NotImplementedError
#
#     @abstractmethod
#     async def approve(self, team: Team, user: Player):
#         raise NotImplementedError
