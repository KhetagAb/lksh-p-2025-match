import logging

from fastapi import APIRouter, Request

from lkshmatch.adapters.base import SportAdapter, ActivityAdapter, Team, Activity
from lkshmatch.di import app_container

api_requests_router = APIRouter(prefix="/api")

@api_requests_router.get("/get_sport_sections")
async def get_sport_sections(_request: Request) -> list | None:
    try:
        sport_adapter = app_container.get(SportAdapter)
        sport_sections = await sport_adapter.get_sport_list()
    except BaseException:
        return None
    return sport_sections


@api_requests_router.get("/get_activities")
async def get_activities_by_sport_section_id(
    _request: Request,
    sport_section_id: int
) -> list[Activity] | None:
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        activities = await activity_adapter.get_activities_by_sport_section(sport_section_id)
    except BaseException as exc:
        logging.warning(exc)
        return None
    return activities


@api_requests_router.get("/get_teams")
async def get_teams_by_activity_id(
    _request: Request,
    activity_id: int
) -> list[Team] | None:
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        teams = await activity_adapter.get_teams_by_activity_id(activity_id)
    except BaseException as exc:
        logging.warning(exc)
        return None
    return teams
