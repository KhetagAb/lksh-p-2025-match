import aiohttp

import core_client
from core_client.api.default import register_player
from core_client.models import RegisterPlayerResponse400, RegisterPlayerResponse200, RegisterPlayerResponse201
from lkshmatch.adapters.base import CoreID, PlayerToRegister, PlayerAdapter, PlayerNotFound, PlayerAlreadyRegister, \
    UnknownError, Player
from lkshmatch.config import settings
from lkshmatch.domain.repositories.player_repository import PlayerRepository

core_client_url = f'{settings.get("CORE_HOST")}:{settings.get("CORE_PORT")}'


class PlayerCoreAdapter(PlayerAdapter):
    def __init__(self):
        # TODO DI
        self.client = core_client.Client(base_url=core_client_url)

    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        # TODO
        players = PlayerRepository().get_players()

        player_name = None
        for i in players:
            if i.tg_username == user.tg_username:
                player_name = i.name
        if player_name is None:
            raise PlayerNotFound()

        return PlayerToRegister(
            tg_username=user.tg_username,
            tg_id=user.tg_id,
            name=player_name
        )

    async def register_user(self, user: PlayerToRegister) -> CoreID:
        response = await register_player.asyncio(
            client=self.client,
            tg_username=user.tg_username,
            tg_id=user.tg_id,
            name=user.name
        )

        if isinstance(response, RegisterPlayerResponse201):
            return response.id
        if isinstance(response, RegisterPlayerResponse200):
            raise PlayerAlreadyRegister
        elif isinstance(response, RegisterPlayerResponse400):
            # todo explain
            raise ValueError("400 error")
        else:
            raise UnknownError

    async def get_player_id(self, user: Player) -> CoreID:
        pass  # TODO
        # async with aiohttp.ClientSession() as session:
        #     query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
        #     response = await session.get(f'{API_URL}/register_user', params=query)
        #
        #     if response.status != 200:
        #         raise UnknownError
        #
        #     data = await response.json()
        #     return int(data['id'])
