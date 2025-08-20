from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_core_teams_by_activity_id_response_200 import GetCoreTeamsByActivityIdResponse200
from ...models.get_core_teams_by_activity_id_response_400 import GetCoreTeamsByActivityIdResponse400
from ...types import Response


def _get_kwargs(
    id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/core/teams/by_activity/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]:
    if response.status_code == 200:
        response_200 = GetCoreTeamsByActivityIdResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = GetCoreTeamsByActivityIdResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]:
    """Получение активности по идентификатору

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]:
    """Получение активности по идентификатору

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]:
    """Получение активности по идентификатору

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]]:
    """Получение активности по идентификатору

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetCoreTeamsByActivityIdResponse200, GetCoreTeamsByActivityIdResponse400]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
