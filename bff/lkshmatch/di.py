from dishka import Provider, Scope, provide

from lkshmatch.adapters.core import (GetPlayersBySportSections,
                                     GetSportSections,
                                     RegisterPlayerInSportSection,
                                     RegisterUser, ValidateRegisterUser)
from lkshmatch.adapters.rest import (RestGetPlayersBySportSections,
                                     RestGetSportSections,
                                     RestRegisterPlayerInSportSection,
                                     RestRegisterUser,
                                     RestValidateRegisterUser)


class AdaptersProvider(Provider):
    scope = Scope.APP

    get_player_by_sport_sections = provide(
        RestGetPlayersBySportSections, provides=GetPlayersBySportSections
    )
    get_sport_sections = provide(
        RestGetSportSections, provides=GetSportSections
    )
    register_player_in_sport_section = provide(
        RestRegisterPlayerInSportSection, provides=RegisterPlayerInSportSection
    )
    register_user = provide(RestRegisterUser, provides=RegisterUser)
    validate_register_user = provide(
        RestValidateRegisterUser, provides=ValidateRegisterUser
    )


def all_providers() -> list[Provider]:
    return [AdaptersProvider()]
