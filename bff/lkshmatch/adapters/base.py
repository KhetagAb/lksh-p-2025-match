from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from lkshmatch.core_client.types import UNSET, Unset

PlayerId = NewType("PlayerId", int)
TeamId = NewType("TeamId", int)
SportSectionId = NewType("SportSectionId", int)
SportSectionName = NewType("SportSectionName", str)


class PlayerNotFound(Exception):
    pass


class PlayerAlreadyRegistered(Exception):
    pass


class TeamIsFull(Exception):
    pass


class NameTeamReserveError(Exception):
    pass


class PlayerAlreadyInTeam(Exception):
    pass


class TeamNotFound(Exception):
    pass


class InsufficientRights(Exception):
    pass


class InvalidParameters(Exception):
    pass


class EnrollmentFinished(Exception):
    pass


class UnknownError(Exception):
    pass


CoreID = int
TgID = int


@dataclass
class Player:
    core_id: CoreID
    name: str
    tg_id: TgID
    tg_username: str


@dataclass
class PlayerToRegister:
    tg_id: TgID
    tg_username: str
    name: str


@dataclass
class SportSection:
    id: int
    name: str
    ru_name: str


@dataclass
class Activity:
    id: int
    title: str
    creator: Player
    description: str | None
    enroll_deadline: datetime | None
    sport_section_id: int


@dataclass
class Team:
    id: int
    name: str
    captain: Player
    members: list[Player]


class PlayerAdapter(ABC):
    @abstractmethod
    async def register_user(self, user: PlayerToRegister) -> CoreID:
        raise NotImplementedError

    @abstractmethod
    async def get_player_by_tg(
        self,
        tg_id: int | Unset = UNSET,
        tg_username: str | Unset = UNSET,
    ) -> Player:
        raise NotImplementedError


# TODO спросить куда это поместить
class PlayerAdminAdapter(ABC):
    @abstractmethod
    async def admin_register_user(
        self,
        user: PlayerToRegister,
        player_info: Player,
    ) -> CoreID:
        raise NotImplementedError


class SportAdapter(ABC):
    @abstractmethod
    async def get_sport_list(self) -> list[SportSection]:
        raise NotImplementedError


class ActivityAdminAdapter(ABC):
    @abstractmethod
    async def create_activity(
        self,
        requester_username: str,
        title: str,
        sport_section_id: int,
        creator_id: int,
        description: str | Unset = UNSET,
        enroll_deadline: datetime | Unset = UNSET,
    ) -> Activity:
        raise NotImplementedError

    @abstractmethod
    async def delete_activity(
        self,
        requester_username: str,
        core_id: CoreID,
    ) -> Activity:
        raise NotImplementedError

    @abstractmethod
    async def update_activity(
        self,
        activity_id: int,
        requester_username: str,
        title: str,
        creator_id: int,
        description: str | Unset = UNSET,
        enroll_deadline: datetime | Unset = UNSET,
    ) -> Activity:
        raise NotImplementedError


class ActivityAdapter(ABC):
    @abstractmethod
    async def get_activities_by_sport_section(
        self,
        sport_section_id: int,
    ) -> list[Activity]:
        raise NotImplementedError

    @abstractmethod
    async def get_activity_by_id(
        self,
        activity_id: int,
    ) -> Activity:
        raise NotImplementedError

    @abstractmethod
    async def get_teams_by_activity_id(
        self,
        activity_id: int,
    ) -> list[Team]:
        raise NotImplementedError

    @abstractmethod
    async def enroll_player_in_activity(
        self,
        activity_id: int,
        player_id: CoreID,
    ) -> Team:
        raise NotImplementedError

    @abstractmethod
    async def leave_player_by_activity(
        self,
        activity_id: int,
        player_id: CoreID,
    ) -> None:
        raise NotImplementedError


class TeamAdapter(ABC):
    @abstractmethod
    async def create_team(
        self,
        section: SportSection,
        user: Player,
        name_team: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def teams(
        self,
        section: SportSection,
    ) -> list[Team]:
        raise NotImplementedError

    @abstractmethod
    async def join_team(
        self,
        team: Team,
        user: Player,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def leave_team(
        self,
        team: Team,
        user: Player,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def approve(
        self,
        team: Team,
        user: Player,
    ) -> None:
        raise NotImplementedError
