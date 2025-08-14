from core_client.models import RegisterPlayerRequest
from lkshmatch.adapters.base import PlayerToRegister


def map_player_to_register_request(user: PlayerToRegister) -> RegisterPlayerRequest:
    return RegisterPlayerRequest(tg_username=user.tg_username, name=user.name, tg_id=user.tg_id)

