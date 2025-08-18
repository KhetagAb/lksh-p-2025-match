from lkshmatch import core_client
from lkshmatch.core_client.api.sport_sections import get_core_sport_list
from lkshmatch.adapters.base import SportAdapter, SportSection, UnknownError
from lkshmatch.adapters.core.mappers.sport_section import map_sport_section


class CoreSportAdapter(SportAdapter):
    def __init__(self, core_client: core_client.Client):
        self.client = core_client

    async def get_sport_list(self) -> list[SportSection]:
        response = await get_core_sport_list.asyncio(client=self.client)
        if response is None:
            raise UnknownError("get all sections return null response")
        sport_result = []
        for sport in response.sports_sections:
            sport_result.append(map_sport_section(sport))
        return sport_result
