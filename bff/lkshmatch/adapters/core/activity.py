from typing import List

import core_client
from core_client.api.activities import (
    get_core_activity_by_sport_section_id,
    post_core_activity_id_enroll, get_core_teams_by_activity_id,
)
from core_client.models import (
    ActivityEnrollPlayerRequest,
    GetCoreActivityBySportSectionIdResponse200,
    GetCoreActivityBySportSectionIdResponse400,
    PostCoreActivityIdEnrollResponse200,
    PostCoreActivityIdEnrollResponse400,
)
from lkshmatch.adapters.base import (
    Activity,
    ActivityAdapter,
    CorePlayer,
    InvalidParameters,
    Team,
    TgID,
    UnknownError,
)
from lkshmatch.config import settings


class CoreActivityAdapter(ActivityAdapter):
    def __init__(self, coreclient: core_client.Client):
        self.client = coreclient

    async def get_activities_by_sport_section(self, sport_section_id: int) -> List[Activity]:
        response = await get_core_activity_by_sport_section_id.asyncio(client=self.client, id=sport_section_id)
        if isinstance(response, GetCoreActivityBySportSectionIdResponse400):
            raise InvalidParameters(f"get activity by sport section id returns 400 response: {response.message}")
        if not isinstance(response, GetCoreActivityBySportSectionIdResponse200):
            raise UnknownError("get activity by sport section id returns unknown response")
        activities = []
        for activity in response.activities:
            activities.append(
                Activity(
                    id=activity.id,
                    title=activity.title,
                    description=activity.description,
                    creator=CorePlayer(
                        core_id=activity.creator.core_id,
                        tg_id=activity.creator.tg_id,
                    ),
                )
            )
        return activities

    # TODO перенести в TeamsAdapter
    async def get_teams_by_activity_id(self, activity_id: int) -> List[Team]:
        response = await get_core_teams_by_activity_id.asyncio(client=self.client, id=activity_id)
        if isinstance(response, GetCoreTeamsByActivityIdResponse400):
            raise InvalidParameters(f"get teams by activity id returns 400 response: {response.message}")
        if not isinstance(response, GetCoreTeamsByActivityIdResponse200):
            raise UnknownError("get teams by activity id returns unknown response")
        teams = []
        # TODO:issue98
        for team in response.teams:
            teams.append(
                Team(
                    id=team.id,
                    name=team.name,
                    capitan=CorePlayer(
                        core_id=team.captain.core_id,
                        tg_id=team.captain.tg_id,
                    ),
                    members=[
                        CorePlayer(
                            core_id=member.core_id,
                            tg_id=member.tg_id,
                        )
                        for member in team.members
                    ],
                )
            )
        return teams

    async def enroll_player_in_activity(self, activity_id: int, player_tg_id: TgID) -> Team:
        response = await post_core_activity_id_enroll.asyncio(
            client=self.client, id=activity_id, body=ActivityEnrollPlayerRequest(tg_id=player_tg_id)
        )
        if isinstance(response, PostCoreActivityIdEnrollResponse400):
            raise InvalidParameters(f"enroll player in activity returns 400 response: {response.message}")
        if not isinstance(response, PostCoreActivityIdEnrollResponse200):
            raise UnknownError("enroll player in activity  returns unknown response")

        team = response.team
        return Team(
            id=team.id,
            name=team.name,
            capitan=CorePlayer(
                core_id=team.captain.core_id,
                tg_id=team.captain.tg_id,
            ),
            members=[
                CorePlayer(
                    core_id=member.core_id,
                    tg_id=member.tg_id,
                )
                for member in team.members
            ],
        )
