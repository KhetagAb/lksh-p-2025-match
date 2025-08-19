from lkshmatch.adapters import base as domain
from lkshmatch.core_client import models as api


def map_player_to_register_request(user: domain.PlayerToRegister) -> api.RegisterPlayerRequest:
    return api.RegisterPlayerRequest(tg_username=user.tg_username, name=user.name, tg_id=user.tg_id)

def map_player_from_api(user:api.Player) -> domain.Player:
    return domain.Player(core_id=user.core_id,name=user.name,tg_id=user.tg_id,tg_username=user.tg_username)