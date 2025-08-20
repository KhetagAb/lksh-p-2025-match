import pytest
import pytest_asyncio
import pytest_httpserver
import requests

from lkshmatch import core_client
from lkshmatch.core_client.models import sport_section as sport_api
from lkshmatch.core_client.api.sport_sections import get_core_sport_list
from lkshmatch.adapters.base import SportAdapter, SportSection, UnknownError
from lkshmatch.adapters.core.mappers.sport_section import map_sport_section
from lkshmatch.adapters.core.sport_sections import CoreSportAdapter
from core_client.models.get_core_sport_list_response_200 import GetCoreSportListResponse200

@pytest.fixture(scope="module")
def test_server():
    with pytest_httpserver.HTTPServer() as httpserver:
        yield httpserver

@pytest.fixture(scope="module")
def activity_adapter(test_server):
    client = core_client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CoreSportAdapter(client)


@pytest.mark.parametrize("list_sport", [[{"id":1, "name": "one", "ru_name": "один"}, {"id":2, "name": "two", "ru_name": "два"}]])
async def test_get_sport_list(activity_adapter, test_server, list_sport: list[dict]):
    test_server.expect_request(
        "/core/sport/list"
    ).respond_with_json({"sports_sections": list_sport}, status=200)

    test_resoult = await activity_adapter.get_sport_list()
    for i in range(2):
        assert (len(test_resoult) == 2 and test_resoult[i].id == list_sport[i]["id"]
                and test_resoult[i].name == list_sport[i]["name"] and test_resoult[i].ru_name == list_sport[i]["ru_name"])

    test_server.clear()

async def test_get_sport_list_error(activity_adapter, test_server):
    with pytest.raises(UnknownError):
        test_server.expect_request(
            "/core/sport/list"
        ).respond_with_data(status=400)

        test_resoult = await activity_adapter.get_sport_list()
