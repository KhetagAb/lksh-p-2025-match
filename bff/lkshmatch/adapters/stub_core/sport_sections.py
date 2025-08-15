from lkshmatch.adapters.base import SportAdapter, SportSection


class PlayerRegisterInfo:
    pass


class StubSportAdapter(SportAdapter):
    async def get_sport_list(self) -> list[SportSection]:
        return [
            SportSection(0, "Volleyball", "Волейбол"),
            SportSection(1, "Football", "Футбол"),
            SportSection(2, "Lksh_shooting", "Стрельба"),
        ]
