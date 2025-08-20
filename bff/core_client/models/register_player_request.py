from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RegisterPlayerRequest")


@_attrs_define
class RegisterPlayerRequest:
    """
    Attributes:
        tg_username (str):
        name (str):
        tg_id (int):
    """

    tg_username: str
    name: str
    tg_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tg_username = self.tg_username

        name = self.name

        tg_id = self.tg_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tg_username": tg_username,
                "name": name,
                "tg_id": tg_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tg_username = d.pop("tg_username")

        name = d.pop("name")

        tg_id = d.pop("tg_id")

        register_player_request = cls(
            tg_username=tg_username,
            name=name,
            tg_id=tg_id,
        )

        register_player_request.additional_properties = d
        return register_player_request

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
