import aiohttp

from lkshmatch.domain.repositories.player_repository import PlayerRepository
from lkshmatch.adapters.core import (ValidateRegisterPlayer, PlayerAddInfo, UnknownError, RegisterPlayer,
                                     PlayerRegisterInfo, PlayerAlreadyRegister, GetPlayerId, API_URL)
from lkshmatch.adapters.sport_sections import PlayerNotFoundResponse


class RestGetPlayerId(GetPlayerId):
    async def get_player_id(self, user: PlayerAddInfo) -> int:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(f'{API_URL}/register_user', params=query)

            if response.status != 200:
                raise UnknownError

            data = await response.json()
            return int(data['id'])


class RestValidateRegisterPlayer(ValidateRegisterPlayer):
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        players = PlayerRepository().get_player()

        ans = ""
        for i in players:
            if i.tg_username == user.tg_username:
                ans = i.name
        if ans == "":
            raise PlayerNotFoundResponse

        return ans


class RestRegisterPlayer(RegisterPlayer):
    async def register_user(self, user: PlayerAddInfo) -> PlayerRegisterInfo:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(f'{API_URL}/register_user', params=query)

            if response.status == 409:
                raise PlayerAlreadyRegister
            if response.status != 200:
                raise UnknownError

            data = await response.json()
            return PlayerRegisterInfo(data["name"], int(data['id']))
