from lkshmatch import core_client
from lkshmatch.adapters.base import (
    CoreID,
    InvalidParameters,
    Player,
    PlayerAdapter,
    PlayerAlreadyRegistered,
    PlayerToRegister,
    UnknownError,
)
from lkshmatch.adapters.core.mappers.player import (
    map_player_to_register_request,
    map_player_from_api,
)
from lkshmatch.core_client.api.players import get_core_player_by_tg, register_player
from lkshmatch.core_client.models import (
    GetCorePlayerByTgResponse200,
    GetCorePlayerByTgResponse400,
    RegisterPlayerResponse200,
    RegisterPlayerResponse201,
)
from lkshmatch.core_client.types import Unset, UNSET


class CorePlayerAdapter(PlayerAdapter):
    def __init__(self, coreclient: core_client.Client):
        self.client = coreclient

    async def register_user(self, user: PlayerToRegister) -> CoreID:
        response = await register_player.asyncio(
            client=self.client,
            body=map_player_to_register_request(user),
        )

        if isinstance(response, RegisterPlayerResponse200):
            raise PlayerAlreadyRegistered("player already register")
        elif isinstance(response, RegisterPlayerResponse201):
            return response.id
        raise UnknownError(f"register user return unknown response: {response}")

    async def get_player_by_tg(
            self,
            tg_id: int | Unset = UNSET,
            tg_username: str | Unset = UNSET,
    ) -> Player:
        response = await get_core_player_by_tg.asyncio(
            client=self.client, tg_id=tg_id, tg_username=tg_username
        )

        if isinstance(response, GetCorePlayerByTgResponse400):
            raise InvalidParameters(
                f"get player by tg return 400 response: {response.message}"
            )
        if not isinstance(response, GetCorePlayerByTgResponse200):
            raise UnknownError(f"get player by tg return unknown response: {response}")

        player = response.player
        return map_player_from_api(player)
