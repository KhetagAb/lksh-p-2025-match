from typing import Any

from lkshmatch.core_client.types import UNSET, Unset


def as_none(value: Any | Unset) -> Any | None:
    return value if value != UNSET else None
