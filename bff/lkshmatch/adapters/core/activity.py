import core_client
from core_client.api.activities import (
    get_core_activities_by_sport_section_id,
    get_core_teams_by_activity_id,
    post_core_activity_id_enroll, post_core_activity_create, post_core_activity_delete_by_id,
    post_core_activity_update_by_id,
)
from core_client.models import (
    ActivityEnrollPlayerRequest,
    GetCoreActivitiesBySportSectionIdResponse200,
    GetCoreActivitiesBySportSectionIdResponse400,
    GetCoreTeamsByActivityIdResponse200,
    GetCoreTeamsByActivityIdResponse400,
    PostCoreActivityIdEnrollResponse200,
    PostCoreActivityIdEnrollResponse400, CreateActivityRequest, PostCoreActivityCreateResponse200,
    PostCoreActivityCreateResponse400, UpdateActivityRequest, PostCoreActivityUpdateByIdResponse200,
    PostCoreActivityUpdateByIdResponse400, PostCoreActivityDeleteByIdResponse400,
)
from lkshmatch.adapters.base import (
    Activity,
    ActivityAdapter,
    InvalidParameters,
    PlayerAlreadyInTeam,
    Team,
    TgID,
    UnknownError, ActivityAdminAdapter, )
from lkshmatch.adapters.core.mappers.activity import map_team, map_activity
from lkshmatch.admin.admin_privilege import PrivilegeChecker
from lkshmatch.config import settings


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
            desc: str = activity.description if activity.description else ""
            activities.append(Activity(activity.id, activity.title, desc, map_core_player(activity.creator)))
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

    async def enroll_player_in_activity(self, activity_id: int, player_tg_id: TgID) -> Team:
        response = await post_core_activity_id_enroll.asyncio(
            client=self.client, id=activity_id, body=ActivityEnrollPlayerRequest(tg_id=player_tg_id)
        )
        if isinstance(response, PostCoreActivityIdEnrollResponse400):
            raise InvalidParameters(f"enroll player in activity returns 400 response: {response.message}")
        if isinstance(response, PostCoreActivityIdEnrollResponse409):
            raise PlayerAlreadyInTeam(f"Player is already enrolled in a team for this activity: {response.message}")
        if not isinstance(response, PostCoreActivityIdEnrollResponse200):
            raise UnknownError("enroll player in activity  returns unknown response")

        team = response.team
        return map_team(team)


class CoreActivityAdminAdapter(ActivityAdminAdapter):
    def __init__(self):
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        self.client = core_client.Client(base_url=core_client_url)

    async def create_activity(self, title: str, sport_section_id: int, creator_id: int, description: str) -> Activity:
        headers = PrivilegeChecker.check_admin(creator_id)
        response = await post_core_activity_create.asyncio(client=self.client,
                                                           body=CreateActivityRequest(title, sport_section_id,
                                                                                      creator_id), headers=headers)
        if isinstance(response, PostCoreActivityCreateResponse400):
            raise InvalidParameters(f"create activity return 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityCreateResponse200):
            raise UnknownError("create activity return unknown response")

        activity = response.activity
        return map_activity(activity)

    async def delete_activity(self, creator_id: int) -> Activity:
        headers = PrivilegeChecker.check_admin(creator_id)
        response = await post_core_activity_delete_by_id.asyncio(client=self.client, headers=headers)
        if isinstance(response, PostCoreActivityDeleteByIdResponse400):
            raise InvalidParameters(f"delete activity return 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityDeleteByIdResponse200):
            raise UnknownError("delete activity return unknown response")

        activity = response.activity
        return map_activity(activity)

    async def update_activity(self, title: str, description: str, creator_id: int) -> Activity:
        headers = PrivilegeChecker.check_admin(creator_id)
        response = await post_core_activity_update_by_id.asyncio(client=self.client,
                                                                 body=UpdateActivityRequest(title, description),
                                                                 headers=headers)
        if isinstance(response, PostCoreActivityUpdateByIdResponse400):
            raise InvalidParameters(f"update activity return 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityUpdateByIdResponse200):
            raise UnknownError("update activity return unknown response")

        activity = response.activity
        return map_activity(activity)
