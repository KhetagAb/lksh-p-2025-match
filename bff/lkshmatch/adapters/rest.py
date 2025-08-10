from bff.lkshmatch.adapters.core import (ValidateRegisterUser, RegisterUser, GetSportSections, GetPlayersBySportSections, Player,
                   PlayerAddInfo, SportSection, RegisterPlayerInSportSection,
                   PlayerNotFound, UnknownError, PlayerRegisterInfo, Team, NameTeamReserveError,
                    PlayerAlreadyInTeam, CreateTeam, JoinTeam)
import aiohttp
from bff.lkshmatch.config import settings
import json

#TODO: Исправить, как - спросить у Хета
API_URL = str(settings.CORE_HOST) + ':' + str(settings.CORE_PORT)


class PlayerNotFoundResponse(PlayerNotFound):
    pass


class ErrorResponse(UnknownError):
    pass


class RestValidateRegisterUser(ValidateRegisterUser):
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(API_URL, params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerNotFoundResponse
            if response.status != 200:
                raise UnknownError

            return data["name"]


class RestRegisterUser(RegisterUser):
    async def register_user(self, user: PlayerAddInfo) -> PlayerRegisterInfo:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(API_URL, params=query)

            if response.status != 200:
                raise UnknownError

            data = await response.json()
            return PlayerRegisterInfo(data["name"], int(data['id']))


class RestGetSportSections(GetSportSections):
    async def get_sections(self) -> list[SportSection]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError

            data = await response.json()
            data_section = []
            for i in data:
                data_section.append(SportSection(i[0], i[1]))
            return data_section


class RestGetPlayersBySportSections(GetPlayersBySportSections):
    async def list_from_sport_sections(self, section: SportSection) -> list[Player]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError

            data = await response.json()
            data_players = []
            for i in data:
                data_players.append(Player(i))
            return data_players


class RestRegisterPlayerInSportSection(RegisterPlayerInSportSection):
    async def register_player_in_sport_sectoin(self, section: SportSection, user_id: PlayerRegisterInfo) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError

class RestCreateTeam(CreateTeam):
    async def create_team(self, section: SportSection, user: PlayerRegisterInfo, name_team: str) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"name_sport_section": section.en_name, "name_team": name_team, "id": user.id}
            response = await session.get(API_URL, params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerAlreadyInTeam

            if response.status != 200:
                raise UnknownError

class RestGetTeams(Team):
    async def teams(self, section: SportSection) -> list[Team]:
        async with aiohttp.ClientSession() as session:
            query = {"name_sport_section": section.en_name}
            response = await session.get(API_URL, params=query)

            if response.status != 200:
                raise UnknownError

            data = await response.json()
            data_team = []
            for i in data:
                data_team.append(Team(data['name'], data['id'], section.en_name, data['capitan_id']))
            return data_team

class RestJoinTeam(JoinTeam):
    async def join_team(self, team: Team, user: PlayerRegisterInfo) -> int:
        async with aiohttp.ClientSession() as session:
            query = {"id_team": team.id, "id_user": user.id}
            response = await session.get(API_URL, params=query)

            if response.status != 200:
                raise UnknownError

            data = await response.json()
            data_team = []
            for i in data:
                data_team.append(Team(data['name'], data['id'], section.en_name, data['capitan_id']))
            return data_team


class LeaveTeam(ABC):
    @abstractmethod
    async def leave_team(self, team: Team, user: PlayerRegisterInfo) -> None:
        raise NotImplementedError

class Approve(ABC):
    @abstractmethod
    async def approve(self, team: Team, user: PlayerRegisterInfo):
        raise NotImplementedError