import logging
import os

from pymongo import MongoClient
from sqlalchemy.testing.suite.test_reflection import users

import core_client
from core_client.api.default import register_player
from core_client.models import RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse400
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
from lkshmatch.repositories.mongo.players import MongoLKSHStudentsRepository


class CorePlayerAdapter(PlayerAdapter):
    def __init__(self):
        # TODO DI
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        mongo_client = MongoClient(host=os.getenv("MATCH_MONGO_URI"))
        self.client = core_client.Client(base_url=core_client_url)
        self.lksh_config = MongoLKSHStudentsRepository(mongo_client)

    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        print(f'validating user to be registered with username={user.tg_username} and id={user.tg_id}')
        students = self.lksh_config.get_players()
        print(f'found {len(students)} students in lksh base')
        for student in students:
            if student.tg_username == user.tg_username:
                return PlayerToRegister(tg_username=user.tg_username, tg_id=user.tg_id, name=student.name)
        raise PlayerNotFound()

    async def register_user(self, user: PlayerToRegister) -> CoreID:
        response = await register_player.asyncio(
            client=self.client, tg_username=user.tg_username, tg_id=user.tg_id, name=user.name
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
