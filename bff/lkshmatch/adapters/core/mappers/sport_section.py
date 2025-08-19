from lkshmatch.adapters import base as domain
from lkshmatch.core_client import models


def map_sport_section(sport: models.SportSection) -> domain.SportSection:
    return domain.SportSection(id=sport.id, name=sport.name, ru_name=sport.ru_name)
