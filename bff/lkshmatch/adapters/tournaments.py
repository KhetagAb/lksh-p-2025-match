from typing import List

import aiohttp

from bff.lkshmatch.adapters.core import CreateTournament, API_URL, UnknownError, GetAllListTournament, Tournament, \
    TournamentInterval, SportSectionName, GetListTournament, RegisterTeamInTournament, TeamId, RemoveTournament, \
    ModifyTournament, UnregisterTeamInTournament


class RestCreateTournament(CreateTournament):
    async def create_tournament(self, data_tournament: TournamentInterval, sport_name: SportSectionName) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestGetAllListTournament(GetAllListTournament):
    async def get_all_list_tournament(self) -> List[Tournament]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["tournaments"]


# TODO посмотреть
class RestGetListTournament(GetListTournament):
    async def get_list_tournament(self, sport_name: SportSectionName) -> List[Tournament]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["tournaments"]


class RestRegisterTeamInTournament(RegisterTeamInTournament):
    async def register_team_in_tournament(self, tournament: Tournament, team_id: TeamId) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestUnregisterTeamInTournament(UnregisterTeamInTournament):
    async def unregister_team_in_tournament(self, tournament: Tournament, team_id: TeamId) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestRemoveTournament(RemoveTournament):
    async def remove_tournament(self, tournament: Tournament) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError


class RestModifyTournament(ModifyTournament):
    async def modify_tournament(self, tournament: Tournament) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise UnknownError
