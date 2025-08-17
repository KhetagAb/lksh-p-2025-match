import pytest
import ipytest
import pytest_httpserver
import requests
ipytest.autoconfig()

from core_client.api.players import register_player
from core_client.models import RegisterPlayerRequest, RegisterPlayerResponse200, RegisterPlayerResponse201
from lkshmatch.adapters.base import (
    CoreID,
    Player,
    PlayerAdapter,
    PlayerAlreadyRegistered,
    PlayerNotFound,
    PlayerToRegister,
    UnknownError,
)
from lkshmatch.adapters.core.players import CorePlayerAdapter

class test_studet:
    def __int__(self, tg_username: str, tg_id: int, name: str):
        self.tg_username = tg_username
        self.tg_id = tg_id
        self.name = name

class test_mongo:
    def  __init__(self):
        self.players = [test_studet("@XantSid", 1, "Ирина Григоорьева"), test_studet("@Admin", 2, "Имя Админ")]


@pytest.fixture(scope="module")
def test_server():
    pytest_httpserver.httpserver.expect_request(
        "/register_user", method="POST", json={"": 12, "name": "foo"}
    ).respond_with_json({"foo": "bar"})
    yield pytest_httpserver.httpserver

@pytest.fixture(scope="module")
def player_adapter():
    base = test_mongo()
    core_client = f"localhost/{test_server.post}"
    yield CorePlayerAdapter(base, core_client)

@pytest.mark.parametrize("user", [Player("@Xantsid", 1), Player("@Admin", 2)], "name", ["Ирина Григорьева", "Имя Админа"])
def test_validate_register_user(player_adapter, user: Player, name: str):
    test_resoult = player_adapter.validate_register_user(user)
    assert test_resoult.tg_username == user.tg_username and test_resoult.tg_id == user.tg_id and test_resoult.name == name

@pytest.mark.parametrize("user", [Player("@NotExistsUser", 3), Player("@XantSid_withwrongtgid", 4)])
def test_validate_register_user_not_found(player_adapter, user: Player):
    with pytest.raises(PlayerNotFound):
        player_adapter.validate_register_user(user)



@pytest.mark.parametrize("user", [PlayerToRegister("@Xantsid", 1, "Ирина Григорьева"), PlayerToRegister("@Admin", 2, "Имя Админа"),
                                PlayerToRegister("@Reapite", 5, "Ирина Григорьева")],
                                "id", [, ,])
def test_register_user(player_adapter, user: PlayerToRegister, id: int):
    test_resoult = player_adapter.register_user(user)
    assert test_resoult.id == id

@pytest.mark.parametrize("user", [PlayerToRegister("@Xantsid_already", 3, "Ирина Григорьева"), PlayerToRegister("@Admin_already", 4, "Имя Админа")],
                                "id", [, ])
def test_register_user_already_register(player_adapter, user: PlayerToRegister, id: int):
    with pytest.raises(PlayerAlreadyRegistered):
        player_adapter.register_user(user)