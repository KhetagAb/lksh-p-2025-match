from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player import Player


T = TypeVar("T", bound="Activity")


@_attrs_define
class Activity:
    """
    Attributes:
        id (int): Идентификатор активности
        title (str):
        creator (Player): Структура описывающая пользователя
        description (Union[Unset, str]):
    """

    id: int
    title: str
    creator: "Player"
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        creator = self.creator.to_dict()

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "creator": creator,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player import Player

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        creator = Player.from_dict(d.pop("creator"))

        description = d.pop("description", UNSET)

        activity = cls(
            id=id,
            title=title,
            creator=creator,
            description=description,
        )

        activity.additional_properties = d
        return activity

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
