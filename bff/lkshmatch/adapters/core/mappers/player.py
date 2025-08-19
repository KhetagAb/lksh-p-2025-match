from lkshmatch.core_client import models
from lkshmatch.adapters import base as domain


def map_player_to_register_request(user: domain.PlayerToRegister) -> models.RegisterPlayerRequest:
    return models.RegisterPlayerRequest(tg_username=user.tg_username, name=user.name, tg_id=user.tg_id)
