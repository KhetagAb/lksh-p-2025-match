from core_client.models import activity as activity_api
from core_client.models import player as player_api
from core_client.models import team as team_api
from lkshmatch.adapters import base as domain
from lkshmatch.adapters.base import CorePlayer


def map_core_player(player: player_api.Player) -> CorePlayer:
    return CorePlayer(
        core_id=player.core_id,
        tg_id=player.tg_id,
    )


def map_activity(activity: activity_api.Activity) -> domain.Activity:
    return domain.Activity(
        id=activity.id,
        title=activity.title,
        description=activity.description,
        creator=map_core_player(activity.creator),
    )


def map_team(team: team_api.Team) -> domain.Team:
    return domain.Team(
        id=team.id,
        name=team.name,
        captain=map_core_player(team.captain),
        members=[map_core_player(member) for member in team.members],
    )
