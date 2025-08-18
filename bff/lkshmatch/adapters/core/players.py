from typing import Optional

import core_client
from core_client.api.players import register_player, get_core_player_by_tg
from core_client.models import RegisterPlayerResponse200, RegisterPlayerResponse201
from lkshmatch.adapters.base import (
    CoreID,
    Player,
    PlayerAdapter,
    PlayerAlreadyRegistered,
    PlayerNotFound,
    PlayerToRegister,
    UnknownError, TgID,
)
from lkshmatch.adapters.core.mappers.player import map_player_to_register_request, map_player
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository


class CorePlayerAdapter(PlayerAdapter):
    def __init__(self, lksh_config: LKSHStudentsRepository, core_client: core_client.Client):
        self.client = core_client
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

    async def get_player_by_tg(self, tg_id: Optional[TgID], tg_username: Optional[str]) -> Player:
        response = await get_core_player_by_tg.asyncio(
            client=self.client,
            tg_id=tg_id,
            tg_username=tg_username
        )
        #TODO что делать с ошибками
        # if isinstance(response, RegisterPlayerResponse200):
        #     raise PlayerAlreadyRegistered("player already register")
        # elif isinstance(response, RegisterPlayerResponse201):
        #     return response.id
        # raise UnknownError("None response")

        player = response.player
        return map_player(player)
