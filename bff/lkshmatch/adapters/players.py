import aiohttp

from adapters.core import ValidateRegisterPlayer, PlayerAddInfo, UnknownError, RegisterPlayer, \
    PlayerRegisterInfo, API_URL
from .sport_sections import PlayerNotFoundResponse


class RestValidateRegisterPlayer(ValidateRegisterPlayer):
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(f'{API_URL}/validate_register_user', params=query)

            data = await response.json()

            if response.status == 404 and data.count("detail") != 0:
                raise PlayerNotFoundResponse
            if response.status != 200:
                raise UnknownError

            return data["name"]


class RestRegisterPlayer(RegisterPlayer):
    async def register_user(self, user: PlayerAddInfo) -> PlayerRegisterInfo:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(f'{API_URL}/register_user', params=query)

            if response.status != 200:
                raise UnknownError

            data = await response.json()
            return PlayerRegisterInfo(data["name"], int(data['id']))