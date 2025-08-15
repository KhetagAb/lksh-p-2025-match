from core_client.models import RegisterPlayerRequest as api
from lkshmatch.adapters import base as domain


def map_player_to_register_request(user: domain.PlayerToRegister) -> api.RegisterPlayerRequest:
    return api.RegisterPlayerRequest(tg_username=user.tg_username, name=user.name, tg_id=user.tg_id)
