from bff.lkshmatch.adapters.core import (ValidateRegisterUser, RegisterUser, GetSportSections, GetPlayersBySportSections, Player,
                   PlayerAddInfo, SportSection, RegisterPlayerInSportSection,
                   PlayerNotFound, UnknownError, PlayerRegisterInfo, Team, NameTeamReserveError,
                    PlayerAlreadyInTeam, TeamIsFull)
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
    async def get_players_by_sport_sections(self, section: SportSection) -> list[PlayerRegisterInfo]:
        async with aiohttp.ClientSession() as session:
            query = {"name_section": section.en_name}
            response = await session.get(API_URL, params=query)
            if response.status != 200:
                raise UnknownError

            data = await response.json()
            data_players = []
            for i in data:
                data_players.append(PlayerRegisterInfo(i))
            return data_players


class RestRegisterPlayerInSportSection(RegisterPlayerInSportSection):
    async def register_player_in_sport_sectoin(self, section: SportSection, user: PlayerRegisterInfo) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"name_section": section.en_name, "user_id": user.id}
            response = await session.get(API_URL, params=query)
            if response.status != 200:
                raise UnknownError




