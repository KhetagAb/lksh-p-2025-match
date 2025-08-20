from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.player import Player


T = TypeVar("T", bound="Team")


@_attrs_define
class Team:
    """Команда с игроками

    Attributes:
        id (int):
        name (str):
        captain (Player): Структура описывающая пользователя
        members (list['Player']):
    """

    id: int
    name: str
    captain: "Player"
    members: list["Player"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        captain = self.captain.to_dict()

        members = []
        for componentsschemas_player_list_item_data in self.members:
            componentsschemas_player_list_item = componentsschemas_player_list_item_data.to_dict()
            members.append(componentsschemas_player_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "captain": captain,
                "members": members,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player import Player

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        captain = Player.from_dict(d.pop("captain"))

        members = []
        _members = d.pop("members")
        for componentsschemas_player_list_item_data in _members:
            componentsschemas_player_list_item = Player.from_dict(componentsschemas_player_list_item_data)

            members.append(componentsschemas_player_list_item)

        team = cls(
            id=id,
            name=name,
            captain=captain,
            members=members,
        )

        team.additional_properties = d
        return team

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
