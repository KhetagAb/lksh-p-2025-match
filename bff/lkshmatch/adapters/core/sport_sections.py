import os
from typing import List

import aiohttp
from pymongo import MongoClient

import core_client
from core_client.api.default import get_core_sport_get_sport, get_core_sports_get, get_core_sports_get_all
from core_client.types import UNSET, Unset
from lkshmatch.adapters.base import CorePlayer, SportAdapter, SportSection, UnknownError, API_URL
from lkshmatch.config import settings
from lkshmatch.repositories.mongo.students import MongoLKSHStudentsRepository


class PlayerRegisterInfo:
    pass


class CoreSportAdapter(SportAdapter):
    def __init__(self):
        # TODO DI
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        self.client = core_client.Client(base_url=core_client_url)

    async def get_sections(self) -> List[SportSection]:
        response = await get_core_sports_get.asyncio(
            client=self.client
        )
        #TODO че то там
        #if (response.sports_sections != Unset):
        #   return response.sports_sections

    async def get_players_by_sport_sections(self, section: SportSection) -> List[CorePlayer]:
        response = await get_core_sport_get_sport.asyncio(
            client=self.client, sport=section.sport
        )

    async def get_all_sections(self) -> List[SportSection[List[CorePlayer]]]:
        response = await get_core_sports_get_all.asyncio(
            client=self.client
        )




    async def register_player_in_sport_section(self, section: SportSection, user: CorePlayer) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"name_section": section.en_name, "user_id": user.id}
            response = await session.get(f"{API_URL}/register_player_in_sport_section", params=query)
            if response.status != 200:
                raise UnknownError
