from lkshmatch.adapters import base as domain
from lkshmatch.adapters.core.mappers.player import map_player_from_api
from lkshmatch.core_client.models import activity as activity_api
from lkshmatch.core_client.models import team as team_api


def map_activity(activity: activity_api.Activity) -> domain.Activity:
    return domain.Activity(
        id=activity.id,
        title=activity.title,
        description= activity.description if activity.description else None,
        creator=map_player_from_api(activity.creator),
    )


def map_team(team: team_api.Team) -> domain.Team:
    return domain.Team(
        id=team.id,
        name=team.name,
        captain=map_player_from_api(team.captain),
        members=[map_player_from_api(member) for member in team.members],
    )
