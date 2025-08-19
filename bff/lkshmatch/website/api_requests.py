from fastapi import APIRouter, Request
from fastapi.responses import Response

from lkshmatch.adapters.base import SportAdapter, ActivityAdapter
from lkshmatch.di import app_container

from lkshmatch.website.auth.auth import get_user_id_from_token, COOKIE_NAME
from lkshmatch.website.templating import templates

api_requests_router = APIRouter(prefix="/api")

@api_requests_router.get("/get_sport_sections")
async def get_sport_sections_json(_request: Request) -> list | None:
    try:
        sport_adapter = app_container.get(SportAdapter)
        sport_sections = await sport_adapter.get_sport_list()
    except BaseException:
        return None
    return sport_sections


@api_requests_router.get("/get_activity_by_sport_section")
async def get_activity_by_sport_section_json(
    _request: Request,
    sport_section_id: int
) -> list | None:
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        activities = await activity_adapter.get_activities_by_sport_section(sport_section_id)
    except BaseException:
        return None
    return activities