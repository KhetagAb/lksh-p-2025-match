from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.register_player_request import RegisterPlayerRequest
from ...models.register_player_response_200 import RegisterPlayerResponse200
from ...models.register_player_response_201 import RegisterPlayerResponse201
from ...models.register_player_response_500 import RegisterPlayerResponse500
from ...types import Response


def _get_kwargs(
    *,
    body: RegisterPlayerRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/core/player/register",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]:
    if response.status_code == 200:
        response_200 = RegisterPlayerResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = RegisterPlayerResponse201.from_dict(response.json())

        return response_201
    if response.status_code == 500:
        response_500 = RegisterPlayerResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegisterPlayerRequest,
) -> Response[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]:
    """Регистрирует пользователя

    Args:
        body (RegisterPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegisterPlayerRequest,
) -> Optional[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]:
    """Регистрирует пользователя

    Args:
        body (RegisterPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegisterPlayerRequest,
) -> Response[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]:
    """Регистрирует пользователя

    Args:
        body (RegisterPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegisterPlayerRequest,
) -> Optional[Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]]:
    """Регистрирует пользователя

    Args:
        body (RegisterPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RegisterPlayerResponse200, RegisterPlayerResponse201, RegisterPlayerResponse500]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
