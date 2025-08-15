from core_client.models import RegisterPlayerRequest
from lkshmatch.adapters.base import PlayerToRegister

from lkshmatch.adapters import base as domain
from core_client.models import register_player_request as api


def map_player_to_register_request(user: api.RegisterPlayerRequest) -> domain.PlayerToRegister:
    return PlayerToRegister(tg_username=user.tg_username,
                            name=user.name,
                            tg_id=user.tg_id)
