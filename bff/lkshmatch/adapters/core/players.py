import os

from pymongo import MongoClient

import core_client
from core_client.api.players import register_player
from core_client.models import RegisterPlayerRequest, RegisterPlayerResponse200, RegisterPlayerResponse201
from lkshmatch.adapters.base import (
    CoreID,
    Player,
    PlayerAdapter,
    PlayerAlreadyRegistered,
    PlayerNotFound,
    PlayerToRegister,
    UnknownError,
)
from lkshmatch.config import settings
from lkshmatch.repositories.mongo.students import MongoLKSHStudentsRepository


class CorePlayerAdapter(PlayerAdapter):
    def __init__(self, lksh_config: MongoLKSHStudentsRepository, core_client: core_client.Client):
        self.client = core_client
        self.lksh_config = lksh_config

    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        print(f"validating user to be registered with username={user.tg_username} and id={user.tg_id}")
        students = self.lksh_config.get_players()
        print(f"found {len(students)} students in lksh base")
        for student in students:
            if student.tg_username == user.tg_username:
                return PlayerToRegister(tg_username=user.tg_username, tg_id=user.tg_id, name=student.name)
        raise PlayerNotFound()

    async def register_user(self, user: PlayerToRegister) -> CoreID:
        response = await register_player.asyncio(
            client=self.client,
            body=RegisterPlayerRequest(tg_username=user.tg_username, name=user.name, tg_id=user.tg_id),
        )

        if isinstance(response, RegisterPlayerResponse200):
            raise PlayerAlreadyRegistered("player already register")
        elif isinstance(response, RegisterPlayerResponse201):
            return response.id
        raise UnknownError("None response")
