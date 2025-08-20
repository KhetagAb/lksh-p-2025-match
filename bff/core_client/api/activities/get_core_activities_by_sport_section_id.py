from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_core_activities_by_sport_section_id_response_200 import GetCoreActivitiesBySportSectionIdResponse200
from ...models.get_core_activities_by_sport_section_id_response_400 import GetCoreActivitiesBySportSectionIdResponse400
from ...types import Response


def _get_kwargs(
    id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/core/activities/by_sport_section/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]:
    if response.status_code == 200:
        response_200 = GetCoreActivitiesBySportSectionIdResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = GetCoreActivitiesBySportSectionIdResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]:
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
) -> Response[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]:
    """Возвращает список всех активностей по спорту

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]
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
) -> Optional[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]:
    """Возвращает список всех активностей по спорту

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]:
    """Возвращает список всех активностей по спорту

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]
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
) -> Optional[Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]]:
    """Возвращает список всех активностей по спорту

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetCoreActivitiesBySportSectionIdResponse200, GetCoreActivitiesBySportSectionIdResponse400]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
