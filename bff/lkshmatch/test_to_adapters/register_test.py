import pytest
import pytest_asyncio
import pytest_httpserver
import requests

from core_client.api.players import register_player
from core_client.models import RegisterPlayerRequest, RegisterPlayerResponse200, RegisterPlayerResponse201
import core_client
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

class test_student:
    def __init__(self, tg_username: str, tg_id: int, name: str):
        self.tg_username = tg_username
        self.tg_id = tg_id
        self.name = name

class test_mongo:
    def  __init__(self):
        self.players = [test_student("@Xantsid", 1, "Ирина Григорьева"), test_student("@Admin", 2, "Имя Админа")]
    async def get_students(self):
        return self.players

@pytest.fixture(scope="module")
def test_server():
    httpserver = pytest_httpserver.HTTPServer()
    test_param_register_successful = [["@Xantsid", "Ирина Григорьева", 1, 1], ["@Admin", "Имя Админа", 2, 2]]
    for i in test_param_register_successful:
        httpserver.expect_request(
            "/register_player", json={"tg_username": i[0], "name":i[1], "tg_id":i[2]}
        ).respond_with_json({"id": i[3]}, status = 201)

    test_param_register_successful = [["@Xantsid_already", 3, "Ирина Григорьева"], ["@Admin_already", 4, "Имя Админа"]]
    for i in test_param_register_successful:
        httpserver.expect_request(
            "/register_player", json={"tg_username": i[0], "name":i[1], "tg_id":i[2]}
        ).respond_with_data("", status = 200)
    yield httpserver

@pytest.fixture(scope="module")
def player_adapter(test_server):
    base = test_mongo()
    client = core_client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CorePlayerAdapter(base, client)



@pytest.mark.parametrize("user, name", [(Player("@Xantsid", 1),"Ирина Григорьева"), (Player("@Admin", 2), "Имя Админа")],
                         ids=["Ирина Григорьева", "Имя Админа"])
async def test_validate_register_user(player_adapter, user: Player, name: str):
    test_resoult = await player_adapter.validate_register_user(user)
    assert test_resoult.tg_username == user.tg_username and test_resoult.tg_id == user.tg_id and test_resoult.name == name

@pytest.mark.parametrize("user", [Player("@NotExistsUser", 3), Player("@Xantsid_withwrongtgid", 4)])
async def test_validate_register_user_not_found(player_adapter, user: Player):
    with pytest.raises(PlayerNotFound):
        a = await player_adapter.validate_register_user(user)

@pytest.mark.parametrize("user, id_reg", [(PlayerToRegister("@Xantsid", 1, "Ирина Григорьева"), 1), (PlayerToRegister("@Admin", 2, "Имя Админа"), 2)])
async def test_register_user(player_adapter, user: PlayerToRegister, id_reg: int):
    test_resoult = await player_adapter.register_user(user)
    assert test_resoult == id_reg

#@pytest.mark.parametrize("user", [PlayerToRegister("@Xantsid_already", 3, "Ирина Григорьева"), PlayerToRegister("@Admin_already", 4, "Имя Админа")],)
#def test_register_user_already_register(player_adapter, user: PlayerToRegister):
#    with pytest.raises(PlayerAlreadyRegistered):
#        player_adapter.register_user(user)
