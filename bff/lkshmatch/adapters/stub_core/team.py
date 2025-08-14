from lkshmatch.adapters.base import CorePlayer, Player, SportSection, Team, TeamAdapter


class StubTeamAdapter(TeamAdapter):
    async def create_team(self, section: SportSection, user: Player, name_team: str) -> str:
        return "Super Team"

    async def teams(self, section: SportSection) -> list[Team]:
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
