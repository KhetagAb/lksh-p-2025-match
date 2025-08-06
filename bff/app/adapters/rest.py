from .core import (ValidateRegisterUser, RegisterUser, GetSportSections, GetPlayersBySportSections, Player,
                   PlayerAddInfo, PlayerId, SportSection, SportSectionId, RegisterPlayerInSection,
                   PlayerNotFound, AnotherError, PlayerRegisterInfo)
import aiohttp
import json

API_URL = "127.0.0.1:3000"


class PlayerNotFoundResponse(PlayerNotFound):
    pass


class ErrorResponse(AnotherError):
    pass


class RestValidateRegisterUser(ValidateRegisterUser):
    async def validate_register_user(self, user: PlayerAddInfo) -> str:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(API_URL, params=query)

            if response.status == 404:
                # TODO проверять что это именно не найденный пользователь
                raise PlayerNotFoundResponse
            if response.status != 200:
                raise AnotherError

            data = await response.json()
            return data["name"]


class RestRegisterUser(RegisterUser):
    async def register_user(self, user: PlayerAddInfo) -> PlayerRegisterInfo:
        async with aiohttp.ClientSession() as session:
            query = {"tg_username": user.tg_username, "tg_id": user.tg_id}
            response = await session.get(API_URL, params=query)

            if response.status != 200:
                raise AnotherError

            data = await response.json()
            return PlayerRegisterInfo(data["name"], int(data['id']))


class RestGetSportSections(GetSportSections):
    async def get_sections(self) -> list[SportSection]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise AnotherError

            data = await response.json()
            return data["sections"]


class RestGetPlayersBySportSections(GetPlayersBySportSections):
    async def list_from_sport_sections(self, section_id: SportSectionId) -> list[Player]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(API_URL)
            if response.status != 200:
                raise AnotherError

            data = response.json()
            return data["players"]