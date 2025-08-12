from dishka import Provider, Scope, provide

from bff.lkshmatch.adapters.core import (GetPlayersBySportSections,
                                     GetSportSections,
                                     RegisterPlayerInSpotrSection,
                                     RegisterPlayer, ValidateRegisterPlayer)
from bff.lkshmatch.adapters.sport_sections import (RestGetPlayersBySportSections,
                                     RestGetSportSections,
                                     RestRegisterPlayerInSportSection)
from bff.lkshmatch.adapters.players import(RestRegisterPlayer,
                                     RestValidateRegisterPlayer)


class AdaptersProvider(Provider):
    scope = Scope.APP

    get_player_by_sport_sections = provide(
        RestGetPlayersBySportSections, provides=GetPlayersBySportSections
    )
    get_sport_sections = provide(
        RestGetSportSections, provides=GetSportSections
    )
    register_player_in_sport_section = provide(
        RestRegisterPlayerInSportSection, provides=RegisterPlayerInSpotrSection
    )
    register_user = provide(RestRegisterPlayer, provides=RegisterPlayer)
    validate_register_user = provide(
        RestValidateRegisterPlayer, provides=ValidateRegisterPlayer
    )


def all_providers() -> list[Provider]:
    return [AdaptersProvider()]
