import pytest
import pytest_httpserver
from typing import Generator


import core_client
from lkshmatch.adapters.base import (
    InvalidParameters,
    PlayerAlreadyInTeam,
    UnknownError,
)
from lkshmatch.adapters.core.activity import CoreActivityAdapter

@pytest.fixture(scope="module")
def test_server() -> Generator[pytest_httpserver.HTTPServer]:
    with pytest_httpserver.HTTPServer() as httpserver:
        yield httpserver

@pytest.fixture(scope="module")
def activity_adapter(test_server) -> Generator[CoreActivityAdapter]:
    client = core_client.Client(base_url=f"http://localhost:{test_server.port}")
    yield CoreActivityAdapter(client)


@pytest.mark.parametrize("sport_id, list_activity", [[1, [{"id": 1, "title": "Voleyball",
                                                           "creator": {"core_id": 1, "name": "aboba",
                                                                       "tg_username": "@aboba", "tg_id": 1}},
                                                          {"id": 2, "title": "Strelba",
                                                           "creator": {"core_id": 1, "name": "aboba",
                                                                       "tg_username": "@aboba", "tg_id": 1}}]]])
async def test_get_activities_by_sport_section(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                               sport_id: int, list_activity: list[dict]) -> None:
    test_server.expect_request(
        f"/core/activities/by_sport_section/{sport_id}"
    ).respond_with_json({"activities": list_activity}, status=200)

    test_resoult = await activity_adapter.get_activities_by_sport_section(sport_id)
    for i in range(2):
        assert (len(test_resoult) == 2 and test_resoult[i].id == list_activity[i]["id"] and test_resoult[i].title ==
                list_activity[i]["title"]
                and test_resoult[i].creator.core_id == list_activity[i]["creator"]["core_id"]
                and test_resoult[i].creator.name == list_activity[i]["creator"]["name"]
                and test_resoult[i].creator.tg_username == list_activity[i]["creator"]["tg_username"]
                and test_resoult[i].creator.tg_id == list_activity[i]["creator"]["tg_id"]
                )


@pytest.mark.parametrize("sport_id, message", [[3, "bulk-bulk"]])
async def test_get_activities_by_sport_section_error400(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                                        sport_id: int, message: str) -> None:
    with pytest.raises(InvalidParameters, match=f"get activity by sport section id returns 400 response: {message}"):
        test_server.expect_request(
            f"/core/activities/by_sport_section/{sport_id}"
        ).respond_with_json({"message": message}, status=400)

        await activity_adapter.get_activities_by_sport_section(sport_id)


@pytest.mark.parametrize("sport_id, message", [[4, "bulk-bulk"]])
async def test_get_activities_by_sport_section_error(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                                     sport_id: int, message: str) -> None:
    with pytest.raises(UnknownError, match="get activity by sport section id returns unknown response"):
        test_server.expect_request(
            f"/core/activities/by_sport_section/{sport_id}"
        ).respond_with_json({"message": message}, status=404)

        await activity_adapter.get_activities_by_sport_section(sport_id)


@pytest.mark.parametrize("sport_id, user_tg_id, team", [[1, 1, {"id": 1, "name": "one",
                                                                "captain": {"core_id": 1, "name": "aboba",
                                                                            "tg_username": "@aboba", "tg_id": 1},
                                                                "members": [{"core_id": 1, "name": "aboba",
                                                                             "tg_username": "@aboba", "tg_id": 1}]}]])
async def test_enroll_player_in_activity(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                         sport_id: int, user_tg_id: int, team: dict) -> None:
    test_server.expect_request(
        f"/core/activity/{sport_id}/enroll", json={"id": user_tg_id}
    ).respond_with_json({"team": team}, status=200)

    test_resoult = await activity_adapter.enroll_player_in_activity(sport_id, user_tg_id)
    assert (test_resoult.id == team["id"] and test_resoult.name == team["name"]
            and test_resoult.captain.core_id == team["captain"]["core_id"]
            and test_resoult.captain.name == team["captain"]["name"]
            and test_resoult.captain.tg_username == team["captain"]["tg_username"]
            and test_resoult.captain.tg_id == team["captain"]["tg_id"]
            and len(test_resoult.members) == 1 and test_resoult.captain == test_resoult.members[0]
            )


@pytest.mark.parametrize("sport_id, user_tg_id, message", [[1, 2, "bulk"]])
async def test_enroll_player_in_activity_error400(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                                  sport_id: int, user_tg_id: int, message: str) -> None:
    with pytest.raises(InvalidParameters):
        test_server.expect_request(
            f"/core/activity/{sport_id}/enroll", json={"id": user_tg_id}
        ).respond_with_json({"message": message}, status=400)

        await activity_adapter.enroll_player_in_activity(sport_id, user_tg_id)


@pytest.mark.parametrize("sport_id, user_tg_id, message", [[1, 3, "bulk"]])
async def test_enroll_player_in_activity_error409(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                                  sport_id: int, user_tg_id: int, message: str) -> None:
    with pytest.raises(PlayerAlreadyInTeam):
        test_server.expect_request(
            f"/core/activity/{sport_id}/enroll", json={"id": user_tg_id}
        ).respond_with_json({"message": message}, status=409)

        await activity_adapter.enroll_player_in_activity(sport_id, user_tg_id)


@pytest.mark.parametrize("activity_id, teams", [[1, [{"id": 1, "name": "one",
                                                      "captain": {"core_id": 1, "name": "aboba",
                                                                  "tg_username": "@aboba", "tg_id": 1},
                                                      "members": [
                                                          {"core_id": 1, "name": "aboba", "tg_username": "@aboba",
                                                           "tg_id": 1}]},
                                                     {"id": 2, "name": "two",
                                                      "captain": {"core_id": 2, "name": "abob", "tg_username": "@abob",
                                                                  "tg_id": 2},
                                                      "members": [{"core_id": 2, "name": "abob", "tg_username": "@abob",
                                                                   "tg_id": 2}]}]]])
async def test_get_teams_by_activity_id(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                        activity_id: int, teams: list[dict]) -> None:
    test_server.expect_request(
        f"/core/teams/by_activity/{activity_id}"
    ).respond_with_json({"teams": teams}, status=200)

    test_resoult = await activity_adapter.get_teams_by_activity_id(activity_id)
    for i in range(2):
        assert (test_resoult[i].id == teams[i]["id"] and test_resoult[i].name == teams[i]["name"]
                and test_resoult[i].captain.core_id == teams[i]["captain"]["core_id"]
                and test_resoult[i].captain.name == teams[i]["captain"]["name"]
                and test_resoult[i].captain.tg_username == teams[i]["captain"]["tg_username"]
                and test_resoult[i].captain.tg_id == teams[i]["captain"]["tg_id"]
                and len(test_resoult[i].members) == 1 and test_resoult[i].captain == test_resoult[i].members[0]
                )


@pytest.mark.parametrize("activity_id", [3])
async def test_get_teams_by_activity_id_error400(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                                 activity_id: int) -> None:
    with pytest.raises(InvalidParameters):
        test_server.expect_request(
            f"/core/teams/by_activity/{activity_id}"
        ).respond_with_json({"message": "bulk"}, status=400)

        await activity_adapter.get_teams_by_activity_id(activity_id)

@pytest.mark.parametrize("activity_id", [4])
async def test_get_teams_by_activity_id_error409(activity_adapter: CoreActivityAdapter, test_server: pytest_httpserver.HTTPServer,
                                                 activity_id: int) -> None:
    with pytest.raises(UnknownError):
        test_server.expect_request(
            f"/core/teams/by_activity/{activity_id}"
        ).respond_with_data(status=409)

        await activity_adapter.get_teams_by_activity_id(activity_id)