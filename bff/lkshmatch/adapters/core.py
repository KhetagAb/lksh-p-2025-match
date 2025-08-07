from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NewType

PlayerId = NewType("PlayerId", int)
SectionId = NewType("SectionId", int)


@dataclass
class PlayerAddInfo:
    tg_username: str


@dataclass
class Section:
    id: SectionId
    name: str


@dataclass
class Player:
    name: str
    is_coach: bool


class AddUser(ABC):
    @abstractmethod
    async def add_user(self, user: PlayerAddInfo) -> PlayerId:
        raise NotImplementedError


class GetSections(ABC):
    @abstractmethod
    async def get_sections(self) -> list[Section]:
        raise NotImplementedError


class ListFromSections(ABC):
    @abstractmethod
    async def list_from_sections(self, section_id: SectionId) -> list[Player]:
        raise NotImplementedError
