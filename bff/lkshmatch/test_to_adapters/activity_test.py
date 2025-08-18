import pytest
import pytest_asyncio
import pytest_httpserver
import requests

from core_client.api.players import register_player
from core_client.models import RegisterPlayerRequest, RegisterPlayerResponse200, RegisterPlayerResponse201
import core_client
from lkshmatch.adapters.base import (
    CorePlayer,
    Activity,
    ActivityAdapter,
    InvalidParameters,
    PlayerAlreadyInTeam,
    TgID,
    UnknownError,
)
from core_client.models import team as team_api
from core_client.models import player as player_api
from lkshmatch.adapters.core.activity import CoreActivityAdapter

@pytest.fixture(scope="module")
def test_server():
    with pytest_httpserver.HTTPServer() as httpserver:
        yield httpserver

@pytest.fixture(scope="module")
def activity_adapter(test_server):
    client = core_client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CoreActivityAdapter(client)


# @pytest.mark.parametrize("sport_id, list_activity", [[1, [Activity(1, "Voleyball", "bulk", CorePlayer(1, 2)), Activity(2, "Strelba", "bulk-bulk", CorePlayer(3, 4))]]])
# async def test_get_activities_by_sport_section(activity_adapter, test_server, sport_id: int, list_activity: list[Activity]):
#     test_server.expect_request(
#         f"/core/activities/by_sport_section/{sport_id}"
#     ).respond_with_json({"activity": list_activity}, status=200)
#
#     test_resoult = await activity_adapter.get_activities_by_sport_section(sport_id)
#     assert test_resoult == list_activity
# @pytest.mark.parametrize("sport_id, message", [[3, "bulk-bulk"]])
# async def test_get_activities_by_sport_section(activity_adapter, test_server, sport_id: int, message: str):
#     with pytest.raises(UnknownError, match=f"get activity by sport section id returns 400 response: {message}"):
#         test_server.expect_request(
#             f"/core/activities/by_sport_section/{sport_id}"
#         ).respond_with_json({"message": message}, status=400)
#
#         test_resoult = await activity_adapter.get_activities_by_sport_section(sport_id)
# @pytest.mark.parametrize("sport_id, message", [[4, "bulk-bulk"]])
# async def test_get_activities_by_sport_section(activity_adapter, test_server, sport_id: int, message: str):
#     with pytest.raises(UnknownError, match="get activity by sport section id returns unknown response"):
#         test_server.expect_request(
#             f"/core/activities/by_sport_section/{sport_id}"
#         ).respond_with_json({"message": message}, status=404)
#
#         test_resoult = await activity_adapter.get_activities_by_sport_section(sport_id)




@pytest.mark.parametrize("sport_id, user_tg_id, team", [[1, 1, {"id": 1, "name": "one", "captain": {"coreId":1, "tgId": 1}, "members": [{"coreId":1, "tgId": 1}]}]])
async def test_enroll_player_in_activity(activity_adapter, test_server, sport_id: int, user_tg_id: int, team: dict):
    test_server.expect_request(
        f"/core/activity/{sport_id}/enroll", json={"tg_id": user_tg_id}
    ).respond_with_json({"team": team}, status=200)

    test_resoult = await activity_adapter.enroll_player_in_activity(sport_id, user_tg_id)
    assert test_resoult.id == team['id']

@pytest.mark.parametrize("sport_id, user_tg_id, message", [[1, 2, "bulk"]])
async def test_enroll_player_in_activity_error400(activity_adapter, test_server, sport_id: int, user_tg_id: int, message: str):
    with pytest.raises(InvalidParameters):
        test_server.expect_request(
            f"/core/activity/{sport_id}/enroll", json={"tg_id": user_tg_id}
        ).respond_with_json({"message":message}, status=400)

        test_resoult = await activity_adapter.enroll_player_in_activity(sport_id, user_tg_id)

@pytest.mark.parametrize("sport_id, user_tg_id, message", [[1, 3, "bulk"]])
async def test_enroll_player_in_activity_error409(activity_adapter, test_server, sport_id: int, user_tg_id: int, message: str):
    with pytest.raises(PlayerAlreadyInTeam):
        test_server.expect_request(
            f"/core/activity/{sport_id}/enroll", json={"tg_id": user_tg_id}
        ).respond_with_json({"message":message}, status=409)

        test_resoult = await activity_adapter.enroll_player_in_activity(sport_id, user_tg_id)