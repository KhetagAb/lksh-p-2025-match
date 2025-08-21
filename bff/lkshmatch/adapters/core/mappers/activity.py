from lkshmatch.adapters import base as domain
from lkshmatch.adapters.core.helpers import as_none
from lkshmatch.adapters.core.mappers.player import map_player_from_api
from lkshmatch.core_client.models import activity as activity_api
from lkshmatch.core_client.models import team as team_api


def map_activity(activity: activity_api.Activity) -> domain.Activity:
    return domain.Activity(
        id=activity.id,
        title=activity.title,
        description=as_none(activity.description),
        enroll_deadline=as_none(activity.enroll_deadline),
        creator=map_player_from_api(activity.creator),
        sport_section_id=activity.sport_section_id,
    )


def map_activity_list(activities: list[activity_api.Activity]) -> list[domain.Activity]:
    return [map_activity(activity) for activity in activities]


def map_team(team: team_api.Team) -> domain.Team:
    return domain.Team(
        id=team.id,
        name=team.name,
        captain=map_player_from_api(team.captain),
        members=[map_player_from_api(member) for member in team.members],
    )


def map_team_list(teams: list[team_api.Team]) -> list[domain.Team]:
    return [map_team(team) for team in teams]
