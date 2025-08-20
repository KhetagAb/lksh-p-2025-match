from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.team import Team


T = TypeVar("T", bound="GetCoreTeamsByActivityIdResponse200")


@_attrs_define
class GetCoreTeamsByActivityIdResponse200:
    """
    Attributes:
        teams (list['Team']):
    """

    teams: list["Team"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        teams = []
        for componentsschemas_team_list_item_data in self.teams:
            componentsschemas_team_list_item = componentsschemas_team_list_item_data.to_dict()
            teams.append(componentsschemas_team_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "teams": teams,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.team import Team

        d = dict(src_dict)
        teams = []
        _teams = d.pop("teams")
        for componentsschemas_team_list_item_data in _teams:
            componentsschemas_team_list_item = Team.from_dict(componentsschemas_team_list_item_data)

            teams.append(componentsschemas_team_list_item)

        get_core_teams_by_activity_id_response_200 = cls(
            teams=teams,
        )

        get_core_teams_by_activity_id_response_200.additional_properties = d
        return get_core_teams_by_activity_id_response_200

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
