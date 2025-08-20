from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.sport_section import SportSection


T = TypeVar("T", bound="GetCoreSportListResponse200")


@_attrs_define
class GetCoreSportListResponse200:
    """
    Attributes:
        sports_sections (list['SportSection']):
    """

    sports_sections: list["SportSection"]

    def to_dict(self) -> dict[str, Any]:
        sports_sections = []
        for componentsschemas_sport_section_list_item_data in self.sports_sections:
            componentsschemas_sport_section_list_item = componentsschemas_sport_section_list_item_data.to_dict()
            sports_sections.append(componentsschemas_sport_section_list_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "sports_sections": sports_sections,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sport_section import SportSection

        d = dict(src_dict)
        sports_sections = []
        _sports_sections = d.pop("sports_sections")
        for componentsschemas_sport_section_list_item_data in _sports_sections:
            componentsschemas_sport_section_list_item = SportSection.from_dict(
                componentsschemas_sport_section_list_item_data
            )

            sports_sections.append(componentsschemas_sport_section_list_item)

        get_core_sport_list_response_200 = cls(
            sports_sections=sports_sections,
        )

        return get_core_sport_list_response_200
