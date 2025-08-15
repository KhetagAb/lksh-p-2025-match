from typing import List

from lkshmatch.adapters.base import (
    Activity,
    ActivityAdapter,
    CorePlayer,
    Team,
    TgID,
)


class StubActivityAdapter(ActivityAdapter):
    async def get_activities_by_sport_section(self, sport_section_id: int) -> List[Activity]:
        activities = [
            Activity(
                id=0,
                title="Турнир по спорту 1",
                description="Лучший турнир 1",
                creator=CorePlayer(core_id=10, tg_id=128),
            ),
            Activity(
                id=1,
                title="Турнир по спорту 2",
                description="Лучший турнир 2",
                creator=CorePlayer(core_id=20, tg_id=228),
            ),
            Activity(
                id=2,
                title="Турнир по спорту 3",
                description="Лучший турнир 3",
                creator=CorePlayer(core_id=30, tg_id=328),
            ),
        ]
        return activities

    async def get_teams_by_activity_id(self, activity_id: int) -> List[Team]:
        teams = [
            Team(
                id=0,
                name="Крутая тима 1",
                capitan=CorePlayer(
                    core_id=1,
                    tg_id=1234,
                ),
                members=[
                    CorePlayer(
                        core_id=2,
                        tg_id=3567,
                    ),
                    CorePlayer(
                        core_id=3,
                        tg_id=4567,
                    ),
                ],
            ),
            Team(
                id=1,
                name="Крутая тима 2",
                capitan=CorePlayer(
                    core_id=2,
                    tg_id=2234,
                ),
                members=[
                    CorePlayer(
                        core_id=3,
                        tg_id=8567,
                    ),
                    CorePlayer(
                        core_id=4,
                        tg_id=5567,
                    ),
                ],
            ),
        ]
        return teams

    async def enroll_player_in_activity(self, activity_id: int, player_tg_id: TgID) -> Team:
        return Team(
            id=10,
            name="Тима зе бест",
            capitan=CorePlayer(
                core_id=1123,
                tg_id=2224,
            ),
            members=[
                CorePlayer(
                    core_id=12354,
                    tg_id=78999797,
                )
            ],
        )
