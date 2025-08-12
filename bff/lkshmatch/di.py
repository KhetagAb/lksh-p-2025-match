import os
from typing import Iterable
from dishka import Provider, Scope, provide
from pymongo import MongoClient
from lkshmatch.domain.repositories.admin_repository import AdminRepository
from lkshmatch.domain.repositories.player_repository import PlayerRepository
from lkshmatch.adapters.core import (GetPlayersBySportSections,
                                     GetSportSections,
                                     RegisterPlayerInSpotrSection,
                                     RegisterPlayer, ValidateRegisterPlayer)
from lkshmatch.adapters.sport_sections import (RestGetPlayersBySportSections,
                                               RestGetSportSections,
                                               RestRegisterPlayerInSportSection)
from lkshmatch.adapters.players import (RestRegisterPlayer,
                                        RestValidateRegisterPlayer)
from lkshmatch.repositories.mongo.admins import MongoAdminRepository
from lkshmatch.repositories.mongo.players import MongoPlayerRepository


class MongoProvider(Provider):
    def __init__(self, uri: str, ping: bool = True):
        super().__init__()
        self._uri = uri
        self._ping = ping

    @provide(scope=Scope.APP)
    def mongo_client(self) -> Iterable[MongoClient]:
        client = MongoClient(self._uri, serverSelectionTimeoutMS=5000)
        if self._ping:
            client.admin.command("ping")
        try:
            yield client
        finally:
            client.close()


class MongoRepositoryProvider(Provider):
    scope = Scope.APP
    mongo_admin_repository = provide(
        MongoAdminRepository, provides=AdminRepository)
    mongo_player_repository = provide(
        MongoPlayerRepository, provides=PlayerRepository)


def all_providers() -> list[Provider]:
    mongo_uri = os.getenv('MATCH_MONGO_URI')
    if mongo_uri is None:
        raise ValueError("MATCH_MONGO_URI environment variable is not set")
    return [MongoProvider(mongo_uri), MongoRepositoryProvider()]
