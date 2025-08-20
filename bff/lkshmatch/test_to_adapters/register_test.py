import pytest
import pytest_httpserver

import core_client
from lkshmatch.adapters.base import (
    PlayerAlreadyRegistered,
    PlayerToRegister,
    UnknownError,
)
from lkshmatch.adapters.core.players import CorePlayerAdapter

# class test_student:
#     def __init__(self, tg_username: str, tg_id: int, name: str):
#         self.tg_username = tg_username
#         self.tg_id = tg_id
#         self.name = name
#
# class test_mongo:
#     def  __init__(self):
#         self.players = [test_student("@Xantsid", 1, "Ирина Григорьева"), test_student("@Admin", 2, "Имя Админа")]
#     async def get_students(self):
#         return self.players

@pytest.fixture(scope="module")
def test_server():
    with pytest_httpserver.HTTPServer() as httpserver:
        yield httpserver

@pytest.fixture(scope="module")
def player_adapter(test_server):

    client = core_client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CorePlayerAdapter(client)



# @pytest.mark.parametrize("user, name", [(Player("@Xantsid", 1),"Ирина Григорьева"), (Playe("@Admin", 2), "Имя Админа")],
#                          ids=["Ирина Григорьева", "Имя Админа"])
# async def test_validate_register_user(player_adapter, user: Player, name: str):
#     test_resoult = await player_adapter.get_player_by_tg(user)
#     assert test_resoult.tg_username == user.tg_username and test_resoult.tg_id == user.tg_id and test_resoult.name == name
#
# @pytest.mark.parametrize("user", [Player("@NotExistsUser", 3), PlayerToRegister("@Xantsid_withwrongtgid", 4)])
# async def test_validate_register_user_not_found(player_adapter, user: Player):
#     with pytest.raises(PlayerNotFound):
#         await player_adapter.get_player_by_tg(user)

@pytest.mark.parametrize("user, id_reg", [(PlayerToRegister(tg_username="@Xantsid", tg_id=1, name="Ирина Григорьева"), 1), 
                                          (PlayerToRegister(tg_username="@Admin", tg_id=2, name="Имя Админа"), 2)])
async def test_register_user(player_adapter, test_server, user: PlayerToRegister, id_reg: int):
    test_server.expect_request(
        "/core/player/register", json={"tg_username": user.tg_username , "name": user.name, "tg_id": user.tg_id}
    ).respond_with_json({"id": id_reg}, status=201)

    test_resoult = await player_adapter.register_user(user)
    assert test_resoult == id_reg

@pytest.mark.parametrize("user, id_reg", [[PlayerToRegister(tg_username="@Xantsid_already", tg_id=3, name="Ирина Григорьева"), 1], 
                                          [PlayerToRegister(tg_username="@Admin_already", tg_id=4, name="Имя Админа"), 2]])
async def test_register_user_already_register(player_adapter, test_server, user: PlayerToRegister, id_reg: int):
    with pytest.raises(PlayerAlreadyRegistered, match = "player already register"):
        test_server.expect_request(
            "/core/player/register", json={"tg_username": user.tg_username, "name": user.name, "tg_id": user.tg_id}
        ).respond_with_json({"id": id_reg}, status=200)

        await player_adapter.register_user(user)


@pytest.mark.parametrize("user, id_reg", [[PlayerToRegister(tg_username="@Error", tg_id=5, name="test_error"), 1]])
async def test_register_user_unknow_error(player_adapter, test_server, user: PlayerToRegister, id_reg: int):
    with pytest.raises(UnknownError):
        test_server.expect_request(
            "/core/player/register", json={"tg_username": user.tg_username, "name": user.name, "tg_id": user.tg_id}
        ).respond_with_json({"id": id_reg}, status=400)

        await player_adapter.register_user(user)