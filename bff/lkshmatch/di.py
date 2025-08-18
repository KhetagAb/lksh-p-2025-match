from collections.abc import Iterable
from types import TracebackType

from dishka import Container, Provider, Scope, make_container, provide
from lkshmatch.core_client import Client
from pymongo import MongoClient

from lkshmatch.adapters.base import ActivityAdapter, PlayerAdapter, SportAdapter
from lkshmatch.adapters.core.activity import CoreActivityAdapter
from lkshmatch.adapters.core.players import CorePlayerAdapter
from lkshmatch.adapters.core.sport_sections import CoreSportAdapter
from lkshmatch.config import settings
from lkshmatch.domain.repositories.admin_repository import AdminRepository
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository
from lkshmatch.repositories.mongo.admins import MongoAdminRepository
from lkshmatch.repositories.mongo.students import MongoLKSHStudentsRepository

class CoreClientProvider(Provider):
    def __init__(self, core_host: str, core_port: str):
        super().__init__()
        self.url = f"http://{core_host}:{core_port}"

    @provide(scope=Scope.APP)
    def core_client(self) -> Iterable[Client]:
        client = Client(base_url=self.url)
        yield client


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
        yield client


class MongoRepositoryProvider(Provider):
    scope = Scope.APP
    mongo_admin_repository = provide(MongoAdminRepository, provides=AdminRepository)
    mongo_player_repository = provide(MongoLKSHStudentsRepository, provides=LKSHStudentsRepository)


class RestAllAdapterProvider(Provider):
    scope = Scope.APP
    core_player_adapter = provide(CorePlayerAdapter, provides=PlayerAdapter)
    core_activity_adapter = provide(CoreActivityAdapter, provides=ActivityAdapter)
    core_sport_adapter = provide(CoreSportAdapter, provides=SportAdapter)


def all_providers() -> list[Provider]:
    mongo_host = settings.get("MONGODB_HOST")
    mongo_port = settings.get("MONGODB_PORT")
    mongo_username = settings.get("MONGODB_ROOT_USERNAME")
    mongo_password = settings.get("MONGODB_ROOT_PASSWORD")
    mongo_database = settings.get("MONGODB_DATABASE")
    core_host = settings.get("CORE_HOST")
    core_port = settings.get("CORE_PORT")

    if not all([mongo_username, mongo_password, mongo_database]):
        raise ValueError("MongoDB credentials are not properly set in environment variables")

    mongo_uri = (
        f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?retryWrites=true&w=majority"
    )
    return [
        MongoProvider(mongo_uri),
        MongoRepositoryProvider(),
        RestAllAdapterProvider(),
        CoreClientProvider(core_host, core_port),
    ]


app_container: Container = make_container(*all_providers())