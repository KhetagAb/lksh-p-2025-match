import aiohttp

from bff.lkshmatch.adapters.core import GetSportSections, SportSection, UnknownError, GetPlayersBySportSections, \
    PlayerRegisterInfo, RegisterPlayerInSpotrSection, PlayerNotFound, API_URL


class PlayerNotFoundResponse(PlayerNotFound):
    pass


class ErrorResponse(UnknownError):
    pass


class RestGetSportSections(GetSportSections):
    async def get_sections(self) -> list[SportSection]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{API_URL}/get_sections')
            if response.status != 200:
                raise UnknownError

            data = await response.json()
            return [
                SportSection(name, en_name)
                for name, en_name in data
            ]


# TODO remove
class RestGetPlayersBySportSections(GetPlayersBySportSections):
    async def get_players_by_sport_sections(self, section: SportSection) -> list[PlayerRegisterInfo]:
        async with aiohttp.ClientSession() as session:
            query = {"name_section": section.en_name}
            response = await session.get(f'{API_URL}/get_players_by_sport_sections', params=query)
            if response.status != 200:
                raise UnknownError

            data = await response.json()
            return [
                PlayerRegisterInfo(name, id_player)
                for name, id_player in data
            ]


# TODO remove
class RestRegisterPlayerInSportSection(RegisterPlayerInSpotrSection):
    async def register_player_in_sport_section(self, section: SportSection, user: PlayerRegisterInfo) -> None:
        async with aiohttp.ClientSession() as session:
            query = {"name_section": section.en_name, "user_id": user.id}
            response = await session.get(f'{API_URL}/register_player_in_sport_section', params=query)
            if response.status != 200:
                raise UnknownError
