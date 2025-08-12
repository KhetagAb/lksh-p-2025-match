import aiohttp

from bff.lkshmatch.adapters.core import (CreateTeam, SportSection, UnknownError, PlayerAlreadyInTeam,
    PlayerRegisterInfo, Team, JoinTeam, TeamIsFull, LeaveTeam, Approve, API_URL)
from bff.lkshmatch.adapters.sport_sections import PlayerNotFoundResponse

class RestCreateTeam(CreateTeam):
    async def create_team(self, section: SportSection, user: PlayerRegisterInfo, name_team: str) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"name_sport_section": section.en_name, "name_team": name_team, "id": user.id}
            response = await session.get(f'{API_URL}/create_team', params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerAlreadyInTeam

            if response.status != 200:
                raise UnknownError


class RestGetTeams(Team):
    async def teams(self, section: SportSection) -> list[Team]:
        async with aiohttp.ClientSession() as session:
            query = {"name_sport_section": section.en_name}
            response = await session.get(f'{API_URL}/teams', params=query)

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
            response = await session.get(f'{API_URL}/join_team', params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerAlreadyInTeam

            if response.status == 400 and data.count("detail") != 0:
                raise TeamIsFull

            if response.status != 200:
                raise UnknownError

            return data["id_capitan"]


class RestLeaveTeam(LeaveTeam):
    async def leave_team(self, team: Team, user: PlayerRegisterInfo) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"id_team": team.id, "id_user": user.id}
            response = await session.get(f'{API_URL}/leave_team', params=query)

            if response.status != 200:
                raise UnknownError


class RestApprove(Approve):
    async def approve(self, team: Team, user: PlayerRegisterInfo):
        async with aiohttp.ClientSession() as session:
            query = {"id_team": team.id, "id_user": user.id}
            response = await session.get(f'{API_URL}/approve', params=query)

            if response.status != 200:
                raise UnknownError
