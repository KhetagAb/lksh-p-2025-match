from abc import ABC, abstractmethod
from dataclasses import dataclass
from os.path import extsep
from typing import NewType

PlayerId = NewType("PlayerId", int)
TeamId= NewType("TeamId", int)
SportSectionId = NewType("SportSectionId", int)
SportSectionName = NewType("SportSectionName", str)

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
class data:
    start:int
    end:int


@dataclass
class tournament:
    id:int
    sport_name:SportSectionName

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
    async def get_players_by_sport_sections(self, section_id: SportSection) -> list[PlayerRegisterInfo]:
        raise NotImplementedError

class RegisterPlayerInSpotrSection(ABC):
    @abstractmethod
    async def register_player_in_sport_sectoin(self, user: PlayerAddInfo, section_id: SportSectionId) -> None:
        raise NotImplementedError

class CreateTournament(ABC):
    @abstractmethod
    async def create_tournament(self,data_tournament:data,sport_name:SportSectionName)-> None:
        raise NotImplementedError

class GetAllListTournament(ABC):
    @abstractmethod
    async def get_all_list_tournament(self)-> list[tournament]:
        raise NotImplementedError

class GetListTournament(ABC):
    @abstractmethod
    async def get_list_tournament(self,sport_name:SportSectionName)-> list[tournament]:
        raise NotImplementedError

class RegisterTeamInTournament(ABC):
    @abstractmethod
    async def registration_tesm_in_tournament(self,sport_name:SportSectionName)-> None:
        raise NotImplementedError

class UnRegisterTeamInTournament(ABC):
    @abstractmethod
    async def un_registration_team_in_tournament(self,sport_name:SportSectionName,player_cap_id:PlayerId)-> None:
        raise NotImplementedError


class RemoveTournament(ABC):
    @abstractmethod
    async def remove_tournament(self,sport_name:SportSectionName,player_cap_id:PlayerId)-> None:
        raise NotImplementedError

class ModifyTournament(ABC):
    @abstractmethod
    async def modify_tournament(self,sport_name:SportSectionName,player_cap_id:PlayerId)-> None:
        raise NotImplementedError