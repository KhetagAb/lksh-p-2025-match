from core_client.models import SportSection
from core_client.models import sport_section as api
from lkshmatch.adapters import base as domain


def map_sport_section(sport: api.SportSection) -> domain.SportSection:
    return SportSection(id=sport.id, name=sport.name, ru_name=sport.ru_name)
