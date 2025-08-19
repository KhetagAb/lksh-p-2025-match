from typing import Optional

from lkshmatch.adapters.base import (
    CoreID,
    Player,
    PlayerAdapter,
    PlayerAlreadyRegistered,
    PlayerNotFound,
    PlayerToRegister,
    UnknownError, InvalidParameters,
)
from lkshmatch.adapters.core.mappers.player import map_player_to_register_request, map_player
from lkshmatch.core_client.api.players import get_core_player_by_tg, register_player
from lkshmatch.core_client.models import RegisterPlayerResponse200, RegisterPlayerResponse201, \
    GetCorePlayerByTgResponse400, GetCorePlayerByTgResponse200
from lkshmatch import core_client
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository


class CorePlayerAdapter(PlayerAdapter):
    def __init__(self, lksh_config: LKSHStudentsRepository, coreclient: core_client.Client):
        self.client = coreclient
        self.lksh_config = lksh_config

    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        print(f"validating user to be registered with username={user.tg_username} and id={user.tg_id}")
        students = await self.lksh_config.get_students()
        print(f"found {len(students)} students in lksh base")
        for student in students:
            if student.tg_username == user.tg_username:
                return PlayerToRegister(tg_username=user.tg_username, tg_id=user.tg_id, name=student.name)
        raise PlayerNotFound()

    async def register_user(self, user: PlayerToRegister) -> CoreID:
        response = await register_player.asyncio(
            client=self.client,
            body=map_player_to_register_request(user),
        )

        if isinstance(response, RegisterPlayerResponse200):
            raise PlayerAlreadyRegistered("player already register")
        elif isinstance(response, RegisterPlayerResponse201):
            return response.id
        raise UnknownError("None response")

    async def get_player_by_tg(self, tg_id: Optional[int], tg_username: Optional[str]) -> Player:
        response = await get_core_player_by_tg.asyncio(
            client=self.client,
            tg_id=tg_id,
            tg_username=tg_username
        )

        if isinstance(response, GetCorePlayerByTgResponse400):
            raise InvalidParameters(f"get player by tg return 400 response: {response.message}")
        if not isinstance(response, GetCorePlayerByTgResponse200):
            raise UnknownError("get player by tg  return unknown response")

        player = response.player
        return map_player(player)
