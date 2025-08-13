import os

from pymongo import MongoClient

import core_client
from core_client.api.players import register_player
from core_client.models import RegisterPlayerRequest, RegisterPlayerResponse200, RegisterPlayerResponse201
from lkshmatch.adapters.base import (
    CoreID,
    Player,
    PlayerAdapter,
    PlayerAlreadyRegister,
    PlayerNotFound,
    PlayerToRegister,
    UnknownError,
)
from lkshmatch.config import settings
from lkshmatch.repositories.mongo.students import MongoLKSHStudentsRepository


class CorePlayerAdapter(PlayerAdapter):
    def __init__(self):
        # TODO DI
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        mongo_client = MongoClient(host=os.getenv("MATCH_MONGO_URI"))
        self.client = core_client.Client(base_url=core_client_url)
        self.lksh_config = MongoLKSHStudentsRepository(mongo_client)

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

        if response is None:
            raise UnknownError("register users return None")

        if isinstance(response, RegisterPlayerResponse200):
            raise PlayerAlreadyRegister("player already register")
        elif isinstance(response, RegisterPlayerResponse201):
            return response.id
        raise UnknownError("None response")
