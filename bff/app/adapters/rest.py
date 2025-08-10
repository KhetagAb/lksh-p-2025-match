from bff.app.adapters.core import (ValidateRegisterUser, RegisterUser, GetSportSections, GetPlayersBySportSections,
                                   Player,
                                   PlayerAddInfo, SportSection, SportSectionId, RegisterPlayerInSpotrSection,
                                   PlayerNotFound, UnknownError, PlayerRegisterInfo)

from bff.app.adapters.core import (SportSectionName, CreateTournament, data, UnRegisterTeamInTournament,
                                   RegisterTeamInTournament, RemoveTournament, ModifyTournament, tournament,
                                   SportSectionName, TeamId, GetAllListTournament, GetListTournament)

import aiohttp

from bff.app.config import settings
import json

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
            return data["sections"]


class RestGetPlayersBySportSections(GetPlayersBySportSections):
    async def players_by_sport_sections(self, section_id: SportSectionId) -> list[Player]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["players"]


class RestRegisterPlayerInSpotrSection(RegisterPlayerInSpotrSection):
    async def register_player_in_section(self, section_id: SportSectionId, user_id: PlayerRegisterInfo) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestCreateTournament(CreateTournament):
    async def create_tournament(self, data_tournament: data, sport_name: SportSectionName) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestGetAllListTournament(GetAllListTournament):
    async def get_all_list_tournament(self) -> list[tournament]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["tournaments"]


class RestGetListTournament(GetListTournament):
    async def get_list_tournament(self, sport_name: SportSectionName) -> list[tournament]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["tournaments"]


class RestRegisterTeamInTournament(RegisterTeamInTournament):
    async def registration_tesm_in_tournament(self, tournament_name: tournament, team_id=TeamId) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestUnRegisterTeamInTournament(UnRegisterTeamInTournament):
    async def un_registration_team_in_tournament(self, tournament_name: tournament, team_id=TeamId) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestRemoveTournament(RemoveTournament):
    async def remove_tournament(self, tournament_name: tournament) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestModifyTournament(ModifyTournament):
    async def modify_tournament(self, tournament_name: tournament) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
