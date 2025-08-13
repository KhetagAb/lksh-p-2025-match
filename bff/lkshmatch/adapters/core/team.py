import aiohttp
from pymongo import MongoClient

import core_client
from lkshmatch.adapters.base import TeamAdapter
from lkshmatch.adapters.base import (
    API_URL,
    Approve,
    CreateTeam,
    JoinTeam,
    LeaveTeam,
    PlayerAlreadyInTeam,
    PlayerRegisterInfo,
    SportSection,
    Team,
    TeamIsFull,
    UnknownError,
)
from lkshmatch.config import settings


class CoreTeamAdapter(TeamAdapter):
    def __init__(self):
        # TODO DI
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        mongo_client = MongoClient(host=os.getenv("MATCH_MONGO_URI"))
        self.client = core_client.Client(base_url=core_client_url)

    async def create_team(self, section: SportSection, user: PlayerRegisterInfo, name_team: str) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"name_sport_section": section.en_name, "name_team": name_team, "id": user.id}
            response = await session.get(f"{API_URL}/create_team", params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerAlreadyInTeam

            if response.status != 200:
                raise UnknownError

    async def teams(self, section: SportSection) -> list[Team]:
        async with aiohttp.ClientSession() as session:
            query = {"name_sport_section": section.en_name}
            response = await session.get(f"{API_URL}/teams", params=query)

            if response.status != 200:
                raise UnknownError

            data = await response.json()
            data_team = []
            for i in data:
                data_team.append(Team(data["name"], data["id"], section.en_name, data["capitan_id"]))
            return data_team

    async def join_team(self, team: Team, user: PlayerRegisterInfo) -> int:
        async with aiohttp.ClientSession() as session:
            query = {"id_team": team.id, "id_user": user.id}
            response = await session.get(f"{API_URL}/join_team", params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerAlreadyInTeam

            if response.status == 400 and data.count("detail") != 0:
                raise TeamIsFull

            if response.status != 200:
                raise UnknownError

            return data["id_capitan"]

    async def leave_team(self, team: Team, user: PlayerRegisterInfo) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"id_team": team.id, "id_user": user.id}
            response = await session.get(f"{API_URL}/leave_team", params=query)

            if response.status != 200:
                raise UnknownError

    async def approve(self, team: Team, user: PlayerRegisterInfo):
        async with aiohttp.ClientSession() as session:
            query = {"id_team": team.id, "id_user": user.id}
            response = await session.get(f"{API_URL}/approve", params=query)

            if response.status != 200:
                raise UnknownError



