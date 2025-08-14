from lkshmatch.adapters.base import CorePlayer, Activity, Team


def map_core_player(activity:Activity) -> CorePlayer:
    return CorePlayer(
        core_id=activity.creator.core_id,
        tg_id=activity.creator.tg_id,
    )


def map_activity(activity:Activity) -> Activity:
    return Activity(
        id=activity.id,
        title=activity.title,
        description=activity.description,
        creator=map_core_player(activity)
    )

def map_team(team:Team) -> Team:
    return Team(
        id=team.id,
        name=team.name,
        capitan=CorePlayer(
            core_id=team.captain.core_id,
            tg_id=team.captain.tg_id,
        ),
        members=[
            map_core_player(member)
            for member in team.members
        ],
    )


