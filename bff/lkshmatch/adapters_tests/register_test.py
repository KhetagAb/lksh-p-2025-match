import pytest
import pytest_httpserver
from collections.abc import Generator

from lkshmatch import core_client
from lkshmatch.adapters.base import (
    PlayerAlreadyRegistered,
    PlayerToRegister,
    UnknownError,
)
from lkshmatch.adapters.core.players import CorePlayerAdapter

@pytest.fixture(scope="module")
def test_server() -> Generator[pytest_httpserver.HTTPServer]:
    with pytest_httpserver.HTTPServer() as httpserver:
        yield httpserver

@pytest.fixture(scope="module")
def player_adapter(test_server: pytest_httpserver.HTTPServer) -> Generator[CorePlayerAdapter]:
    client = core_client.client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CorePlayerAdapter(client)


@pytest.mark.parametrize("user, id_reg", [(PlayerToRegister(tg_username="@Xantsid", tg_id=1, name="Ирина Григорьева"), 1), 
                                          (PlayerToRegister(tg_username="@Admin", tg_id=2, name="Имя Админа"), 2)])
async def test_register_user(player_adapter: CorePlayerAdapter, test_server: pytest_httpserver.HTTPServer, user: PlayerToRegister, id_reg: int) -> None:
    test_server.expect_request(
        "/core/player/register", json={"tg_username": user.tg_username , "name": user.name, "tg_id": user.tg_id}
    ).respond_with_json({"id": id_reg}, status=201)

    test_resoult = await player_adapter.register_user(user)
    assert test_resoult == id_reg

@pytest.mark.parametrize("user, id_reg", [[PlayerToRegister(tg_username="@Xantsid_already", tg_id=3, name="Ирина Григорьева"), 1], 
                                          [PlayerToRegister(tg_username="@Admin_already", tg_id=4, name="Имя Админа"), 2]])
async def test_register_user_already_register(player_adapter: CorePlayerAdapter, test_server: pytest_httpserver.HTTPServer, user: PlayerToRegister, id_reg: int) -> None:
    with pytest.raises(PlayerAlreadyRegistered, match = "player already register"):
        test_server.expect_request(
            "/core/player/register", json={"tg_username": user.tg_username, "name": user.name, "tg_id": user.tg_id}
        ).respond_with_json({"id": id_reg}, status=200)

        await player_adapter.register_user(user)


@pytest.mark.parametrize("user, id_reg", [[PlayerToRegister(tg_username="@Error", tg_id=5, name="test_error"), 1]])
async def test_register_user_unknow_error(player_adapter: CorePlayerAdapter, test_server:pytest_httpserver.HTTPServer, user: PlayerToRegister, id_reg: int) -> None:
    with pytest.raises(UnknownError):
        test_server.expect_request(
            "/core/player/register", json={"tg_username": user.tg_username, "name": user.name, "tg_id": user.tg_id}
        ).respond_with_json({"id": id_reg}, status=400)

        await player_adapter.register_user(user)