from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.activity_enroll_player_request import ActivityEnrollPlayerRequest
from ...models.post_core_activity_id_enroll_response_200 import PostCoreActivityIdEnrollResponse200
from ...models.post_core_activity_id_enroll_response_400 import PostCoreActivityIdEnrollResponse400
from ...models.post_core_activity_id_enroll_response_409 import PostCoreActivityIdEnrollResponse409
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: ActivityEnrollPlayerRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/core/activity/{id}/enroll",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
]:
    if response.status_code == 200:
        response_200 = PostCoreActivityIdEnrollResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PostCoreActivityIdEnrollResponse400.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = PostCoreActivityIdEnrollResponse409.from_dict(response.json())

        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
]:
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
    body: ActivityEnrollPlayerRequest,
) -> Response[
    Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
]:
    """Создает команду из одного человека на активность

    Args:
        id (int):
        body (ActivityEnrollPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ActivityEnrollPlayerRequest,
) -> Optional[
    Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
]:
    """Создает команду из одного человека на активность

    Args:
        id (int):
        body (ActivityEnrollPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ActivityEnrollPlayerRequest,
) -> Response[
    Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
]:
    """Создает команду из одного человека на активность

    Args:
        id (int):
        body (ActivityEnrollPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ActivityEnrollPlayerRequest,
) -> Optional[
    Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
]:
    """Создает команду из одного человека на активность

    Args:
        id (int):
        body (ActivityEnrollPlayerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PostCoreActivityIdEnrollResponse200, PostCoreActivityIdEnrollResponse400, PostCoreActivityIdEnrollResponse409]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
