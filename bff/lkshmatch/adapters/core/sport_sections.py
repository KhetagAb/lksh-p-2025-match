from typing import List

import aiohttp

import core_client
from core_client.api.sport_sections import get_core_sport_list
from lkshmatch.adapters.base import API_URL, CorePlayer, SportAdapter, SportSection, UnknownError
from lkshmatch.config import settings


class PlayerRegisterInfo:
    pass


class CoreSportAdapter(SportAdapter):
    def __init__(self):
        # TODO DI
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        self.client = core_client.Client(base_url=core_client_url)

    async def get_all_sections(self) -> List[SportSection]:
        response = await get_core_sport_list.asyncio(client=self.client)
        if response is None:
            raise UnknownError("get all sections return null response")
        sport_result = []
        for sport in response.sports_sections:
            sport_result.append(
                SportSection(
                    id=sport.id,
                    name=sport.name,
                    ru_name=sport.ru_name
                )
            )
        return sport_result

