from core_client.models import SportSection


def map_sport_section(sport:SportSection)->SportSection:
    return SportSection(id=sport.id, name=sport.name, ru_name=sport.ru_name)