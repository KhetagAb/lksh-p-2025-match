from .core import (AddUser, GetSections, ListFromSections, Player,
                   PlayerAddInfo, PlayerId, Section, SectionId)


class StubAddUser(AddUser):
    async def add_user(self, user: PlayerAddInfo) -> PlayerId:
        return 42


class StubGetSections(GetSections):
    async def get_sections(self) -> list[Section]:
        return [
            Section(name="Ultra masters 3000", id=10),
            Section(name="Not masters 4000", id=1002),
        ]


class StubListFromSections(ListFromSections):
    async def list_from_sections(self, section_id: SectionId) -> list[Player]:
        return [
            Player(name="Vasya Petrov", is_coach=False),
            Player(name="SigmaSlav", is_coach=False),
            Player(name="Ronaldo", is_coach=True),
        ]
