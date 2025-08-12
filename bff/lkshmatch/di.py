import os
from collections.abc import Iterable
from typing import List

from dishka import Container, Provider, Scope, make_container, provide
from pymongo import MongoClient

from lkshmatch.adapters.base import PlayerAdapter
from lkshmatch.adapters.core.players import CorePlayerAdapter
from lkshmatch.domain.repositories.admin_repository import AdminRepository
from lkshmatch.domain.repositories.player_repository import LKSHStudentsRepository
from lkshmatch.repositories.mongo.admins import MongoAdminRepository
from lkshmatch.repositories.mongo.players import MongoLKSHStudentsRepository


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
        MongoLKSHStudentsRepository, provides=LKSHStudentsRepository)


class RestAdapterProvider(Provider):
    scope = Scope.APP
    core_player_adapter = provide(
        CorePlayerAdapter, provides=PlayerAdapter)


def all_providers() -> List[Provider]:
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri is None:
        raise ValueError("MONGO_URI environment variable is not set")
    return [MongoProvider(mongo_uri), MongoRepositoryProvider(), RestAdapterProvider()]


app_container: Container = make_container(*all_providers())
