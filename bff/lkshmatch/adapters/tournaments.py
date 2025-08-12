from typing import List

import aiohttp

from bff.lkshmatch.adapters.core import CreateTournament, API_URL, UnknownError, GetAllListTournament, Tournament, \
    TournamentInterval, SportSectionName, GetListTournament, RegisterTeamInTournament, TeamId, RemoveTournament, \
    ModifyTournament, UnregisterTeamInTournament, Admin
from bff.lkshmatch.admin.admin_privilege import PrivilegeChecker
from bff.lkshmatch.repositories.admins import AdminsRepository
from bff.lkshmatch.repositories.mongodb import create_mongodb_client


class RestCreateTournament(CreateTournament):
    def __init__(self, admin_repository: AdminsRepository, privilege_checker: PrivilegeChecker):
        self.admins_repository = admin_repository
        self.privilege_checker = privilege_checker

    async def create_tournament(self, data_tournament: TournamentInterval, sport_name: SportSectionName,
                                player_info: Admin) -> None:
        headers = self.privilege_checker.check_admin(player_info)

        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/create_tournament', headers=headers)
            if response.status != 200:
                raise UnknownError


class RestGetAllListTournament(GetAllListTournament):
    async def get_all_list_tournament(self) -> List[Tournament]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/get_all_list_tournament')
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["tournaments"]


class RestGetListTournament(GetListTournament):
    async def get_list_tournament(self, sport_name: SportSectionName) -> List[Tournament]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/get_list_tournament')
            if response.status != 200:
                raise UnknownError
            data = await response.json()
            return data["tournaments"]


class RestRegisterTeamInTournament(RegisterTeamInTournament):
    async def register_team_in_tournament(self, tournament: Tournament, team_id: TeamId,
                                          player_info: Admin) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/register_team_in_tournament')
            if response.status != 200:
                raise UnknownError


class RestUnregisterTeamInTournament(UnregisterTeamInTournament):
    async def unregister_team_in_tournament(self, tournament: Tournament, team_id: TeamId,
                                            player_info: Admin) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/unregister_team_in_tournament')
            if response.status != 200:
                raise UnknownError


class RestRemoveTournament(RemoveTournament):
    def __init__(self, admin_repository: AdminsRepository, privilege_checker: PrivilegeChecker):
        self.admins_repository = admin_repository
        self.privilege_checker = privilege_checker

    async def remove_tournament(self, tournament: Tournament, player_info: Admin) -> None:
        headers = self.privilege_checker.check_admin(player_info)
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/remove_tournament', headers=headers)
            if response.status != 200:
                raise UnknownError


class RestModifyTournament(ModifyTournament):
    def __init__(self, admin_repository: AdminsRepository, privilege_checker: PrivilegeChecker):
        self.admins_repository = admin_repository
        self.privilege_checker = privilege_checker

    async def modify_tournament(self, tournament: Tournament, player_info: Admin) -> None:
        headers = self.privilege_checker.check_admin(player_info)
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/modify_tournament', headers=headers)
            if response.status != 200:
                raise UnknownError
