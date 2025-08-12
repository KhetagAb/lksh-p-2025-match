import aiohttp

import core_client
from core_client.api.default import register_player
from core_client.models import *
from lkshmatch.adapters.core import (
    API_URL,
    GetPlayerId,
    PlayerAddInfo,
    PlayerAlreadyRegister,
    PlayerRegisterInfo,
    RegisterPlayer,
    UnknownError,
    ValidateRegisterPlayer,
)
from lkshmatch.adapters.sport_sections import PlayerNotFoundResponse
from lkshmatch.domain.repositories.player_repository import PlayerRepository
from lkshmatch.config import settings

core_client_url = f'{settings.get("CORE_HOST")}:{settings.get("CORE_PORT")}'


# class RestGetPlayerId(GetPlayerId):
#     async def get_player_id(self, user: PlayerAddInfo) -> int:
#         client = core_client.Client(base_url=core_client_url)
#
#         core_client.api.default.


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
        client = core_client.Client(base_url=core_client_url)
        response = await register_player.asyncio(
            client=client,
            tg_username=user.tg_username,
            tg_id=user.tg_id,
            name='Зубенко Михаил Петрович'
        )

        if isinstance(response, RegisterPlayerResponse400):
            raise PlayerAlreadyRegister
        elif isinstance(response, RegisterPlayerResponse200):
            return PlayerRegisterInfo(response.name, int(response.id))
        else:
            raise UnknownError
