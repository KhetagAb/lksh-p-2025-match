import pytest
import pytest_httpserver
from typing import Generator

from lkshmatch import core_client
from lkshmatch.adapters.base import UnknownError
from lkshmatch.adapters.core.sport_sections import CoreSportAdapter

@pytest.fixture(scope="module")
def test_server() -> Generator[pytest_httpserver.HTTPServer]:
    with pytest_httpserver.HTTPServer() as httpserver:
        yield httpserver

@pytest.fixture(scope="module")
def activity_adapter(test_server) -> Generator[CoreSportAdapter]:
    client = core_client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CoreSportAdapter(client)


@pytest.mark.parametrize("list_sport", [[{"id":1, "name": "one", "ru_name": "один"}, {"id":2, "name": "two", "ru_name": "два"}]])
async def test_get_sport_list(activity_adapter: CoreSportAdapter, test_server: pytest_httpserver.HTTPServer, list_sport: list[dict]) -> None:
    test_server.expect_request(
        "/core/sport/list"
    ).respond_with_json({"sports_sections": list_sport}, status=200)

    test_resoult = await activity_adapter.get_sport_list()
    for i in range(2):
        assert (len(test_resoult) == 2 and test_resoult[i].id == list_sport[i]["id"]
                and test_resoult[i].name == list_sport[i]["name"] and test_resoult[i].ru_name == list_sport[i]["ru_name"])

    test_server.clear()

async def test_get_sport_list_error(activity_adapter: CoreSportAdapter, test_server: pytest_httpserver.HTTPServer) -> None:
    with pytest.raises(UnknownError):
        test_server.expect_request(
            "/core/sport/list"
        ).respond_with_data(status=400)

        await activity_adapter.get_sport_list()
