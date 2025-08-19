from lkshmatch.adapters.core.mappers.player import map_player
from lkshmatch.core_client.models import activity as activity_api
from lkshmatch.core_client.models import player as player_api
from lkshmatch.core_client.models import team as team_api
from lkshmatch.adapters import base as domain


def map_activity(activity: activity_api.Activity) -> domain.Activity:
    return domain.Activity(
        id=activity.id,
        title=activity.title,
        description= activity.description if activity.description else None,
        creator=map_player(activity.creator),
    )


def map_team(team: team_api.Team) -> domain.Team:
    return domain.Team(
        id=team.id,
        name=team.name,
        captain=map_player(team.captain),
        members=[map_player(member) for member in team.members],
    )
