from lkshmatch import core_client
import datetime
from lkshmatch.adapters.base import (
    Activity,
    ActivityAdapter,
    InvalidParameters,
    PlayerAlreadyInTeam,
    Team,
    EnrollmentFinished,
    UnknownError, ActivityAdminAdapter, CoreID, )
from lkshmatch.adapters.core.admin.admin_privilege import PrivilegeChecker
from lkshmatch.adapters.core.mappers.activity import map_team, map_activity
from lkshmatch.adapters.core.mappers.player import map_player_from_api
from lkshmatch.core_client.api.activities import get_core_teams_by_activity_id, post_core_activity_id_enroll, \
    post_core_activity_create, post_core_activity_delete_by_id, post_core_activity_update_by_id, \
    get_core_activities_by_sport_section_id, post_core_activity_id_leave
from lkshmatch.core_client.models import GetCoreActivitiesBySportSectionIdResponse400, \
    GetCoreActivitiesBySportSectionIdResponse200, GetCoreTeamsByActivityIdResponse400, \
    GetCoreTeamsByActivityIdResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409, \
    PostCoreActivityIdEnrollResponse200, ActivityEnrollPlayerRequest, CreateActivityRequest, \
    PostCoreActivityCreateResponse400, PostCoreActivityCreateResponse200, PostCoreActivityDeleteByIdResponse400, \
    PostCoreActivityDeleteByIdResponse200, PostCoreActivityUpdateByIdResponse200, PostCoreActivityUpdateByIdResponse400, \
    UpdateActivityRequest, ActivityLeavePlayerRequest, PostCoreActivityIdLeaveResponse404, \
    PostCoreActivityIdEnrollResponse403
from lkshmatch.core_client.types import Unset, UNSET


class CoreActivityAdapter(ActivityAdapter):
    def __init__(self, coreclient: core_client.Client):
        self.client = coreclient

    async def get_activities_by_sport_section(self, sport_section_id: int) -> list[Activity]:
        response = await get_core_activities_by_sport_section_id.asyncio(client=self.client, id=sport_section_id)
        if isinstance(response, GetCoreActivitiesBySportSectionIdResponse400):
            raise InvalidParameters(f"get activity by sport section id returns 400 response: {response.message}")
        if not isinstance(response, GetCoreActivitiesBySportSectionIdResponse200):
            raise UnknownError("get activity by sport section id returns unknown response")
        activities: list[Activity] = []
        for activity in response.activities:
            activities.append(Activity(
                id=activity.id,
                title=activity.title,
                creator=map_player_from_api(activity.creator),
                description=activity.description if activity.description else ""
            ))
        return activities

    # TODO перенести в TeamsAdapter
    async def get_teams_by_activity_id(self, activity_id: int) -> list[Team]:
        response = await get_core_teams_by_activity_id.asyncio(client=self.client, id=activity_id)
        if isinstance(response, GetCoreTeamsByActivityIdResponse400):
            raise InvalidParameters(f"get teams by activity id returns 400 response: {response.message}")
        if not isinstance(response, GetCoreTeamsByActivityIdResponse200):
            raise UnknownError("get teams by activity id returns unknown response")
        teams = []
        for team in response.teams:
            teams.append(map_team(team))
        return teams

    async def enroll_player_in_activity(self, activity_id: int, player_id: CoreID) -> Team:
        response = await post_core_activity_id_enroll.asyncio(
            client=self.client, id=activity_id, body=ActivityEnrollPlayerRequest(id=player_id)
        )

        if isinstance(response, PostCoreActivityIdEnrollResponse400):
            raise InvalidParameters(f"enroll player in activity returns 400 response: {response.message}")
        if isinstance(response, PostCoreActivityIdEnrollResponse403):
            raise EnrollmentFinished(f"enrollment is finish: {response.message}")
        if isinstance(response, PostCoreActivityIdEnrollResponse409):
            raise PlayerAlreadyInTeam(f"Player is already enrolled in a team for this activity: {response.message}")
        if not isinstance(response, PostCoreActivityIdEnrollResponse200):
            raise UnknownError("enroll player in activity  returns unknown response")

        team = response.team
        return map_team(team)

    async def leave_player_by_activity(self, activity_id: int, player_id: CoreID) -> None:
        response = await post_core_activity_id_leave.asyncio(
            client=self.client, id=activity_id, body=ActivityLeavePlayerRequest(id=player_id)
        )
        if isinstance(response, PostCoreActivityIdLeaveResponse404):
            raise InvalidParameters(f"leave player by activity returns 404 response: {response.message}")


class CoreActivityAdminAdapter(ActivityAdminAdapter):
    def __init__(self, coreclient: core_client.Client, privilege_checker: PrivilegeChecker):
        self.client = coreclient
        self.privilege_checker = privilege_checker

    async def create_activity(self, requester: int, title: str, sport_section_id: int, creator_id: int,
                              description: str | Unset = UNSET,
                              enroll_deadline: datetime.datetime | Unset = UNSET) -> Activity:
        admin_token = self.privilege_checker.get_admin_token(requester)
        response = await post_core_activity_create.asyncio(client=self.client,
                                                           body=CreateActivityRequest(title, sport_section_id,
                                                                                      creator_id, description,
                                                                                      enroll_deadline),
                                                           privilege_token=admin_token)
        if isinstance(response, PostCoreActivityCreateResponse400):
            raise InvalidParameters(f"create activity return 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityCreateResponse200):
            raise UnknownError("create activity return unknown response")

        activity = response.activity
        return map_activity(activity)

    async def delete_activity(self, requester: int, creator_id: int) -> Activity:
        admin_token = self.privilege_checker.get_admin_token(requester)
        response = await post_core_activity_delete_by_id.asyncio(client=self.client, id=creator_id,
                                                                 privilege_token=admin_token)
        if isinstance(response, PostCoreActivityDeleteByIdResponse400):
            raise InvalidParameters(f"delete activity return 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityDeleteByIdResponse200):
            raise UnknownError("delete activity return unknown response")

        activity = response.activity
        return map_activity(activity)

    async def update_activity(self, requester: int, title: str, creator_id: int,
                              description: str | None = None,
                              enroll_deadline: datetime.datetime | Unset = UNSET) -> Activity:
        admin_token = self.privilege_checker.get_admin_token(requester)
        response = await post_core_activity_update_by_id.asyncio(client=self.client,
                                                                 id=creator_id,
                                                                 body=UpdateActivityRequest(title, description or "",enroll_deadline),
                                                                 privilege_token=admin_token)
        if isinstance(response, PostCoreActivityUpdateByIdResponse400):
            raise InvalidParameters(f"update activity return 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityUpdateByIdResponse200):
            raise UnknownError("update activity return unknown response")

        activity = response.activity
        return map_activity(activity)
