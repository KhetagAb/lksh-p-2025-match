# from typing import List

# import aiohttp
# from pymongo import MongoClient

# import core_client
# from lkshmatch.adapters.base import (
#     API_URL,
#     Admin,
#     SportSectionName,
#     TeamId,
#     Tournament,
#     TournamentInterval,
#     UnknownError,
#     TournamentAdminAdapter,
#     TournamentAdapter
# )
# from lkshmatch.admin.admin_privilege import PrivilegeChecker
# from lkshmatch.domain.repositories.admin_repository import AdminRepository
# from lkshmatch.config import settings
# from lkshmatch.repositories.mongo.students import MongoLKSHStudentsRepository


# class CoreTournamentAdminAdapter(TournamentAdminAdapter):
#     def __init__(self):
#         # TODO DI тоже
#         core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
#         mongo_client = MongoClient(host=os.getenv("MATCH_MONGO_URI"))
#         self.client = core_client.Client(base_url=core_client_url)
#         self.lksh_config = MongoLKSHStudentsRepository(mongo_client)

#     async def create_tournament(
#             self, data_tournament: TournamentInterval, sport_name: SportSectionName, player_info: Admin
#     ) -> None:
#         # TODO исправить датакласс в base
#         response = await create_tournament.asyncio(
#             client=self.client, name=sport_name.name, tg_id=user.tg_id, name=user.name
#         )

#     async def remove_tournament(self, tournament: Tournament, player_info: Admin) -> None:
#         headers = self.privilege_checker.check_admin(player_info)
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(f"{API_URL}/remove_tournament", headers=headers)
#             if response.status != 200:
#                 raise UnknownError

#     async def modify_tournament(self, tournament: Tournament, player_info: Admin) -> None:
#         headers = self.privilege_checker.check_admin(player_info)
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(f"{API_URL}/modify_tournament", headers=headers)
#             if response.status != 200:
#                 raise UnknownError


# class CoreTournamentAdapter(TournamentAdapter):
#     async def get_all_list_tournament(self) -> List[Tournament]:
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(f"{API_URL}/get_all_list_tournament")
#             if response.status != 200:
#                 raise UnknownError
#             data = await response.json()
#             return data["tournaments"]

#     async def get_list_tournament(self, sport_name: SportSectionName) -> List[Tournament]:
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(f"{API_URL}/get_list_tournament")
#             if response.status != 200:
#                 raise UnknownError
#             data = await response.json()
#             return data["tournaments"]

#     async def register_team_in_tournament(self, tournament: Tournament, team_id: TeamId, player_info: Admin) -> None:
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(f"{API_URL}/register_team_in_tournament")
#             if response.status != 200:
#                 raise UnknownError

#     async def unregister_team_in_tournament(self, tournament: Tournament, team_id: TeamId,
#                                             player_info: Admin) -> None:
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(f"{API_URL}/unregister_team_in_tournament")
#             if response.status != 200:
#                 raise UnknownError


