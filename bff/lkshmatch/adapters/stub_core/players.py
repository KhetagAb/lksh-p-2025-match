from lkshmatch.adapters.base import (
    CoreID,
    Player,
    PlayerAdapter,
    PlayerToRegister,
)


class StubPlayerAdapter(PlayerAdapter):
    async def validate_register_user(self, user: Player) -> PlayerToRegister:
        return PlayerToRegister(user.tg_username, user.tg_id, "Vasya Pupkin")

    async def register_user(self, user: PlayerToRegister) -> CoreID:
        return 228
