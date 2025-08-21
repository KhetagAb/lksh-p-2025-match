import logging

from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse

from lkshmatch.adapters.base import Activity, ActivityAdapter, SportAdapter, Team
from lkshmatch.di import app_container
from lkshmatch.website.templating import templates_path

api_requests_router = APIRouter(prefix="/api")


@api_requests_router.get("/ckeditor.js")
async def get_ckeditor_js(request: Request) -> Response:
    return FileResponse(templates_path + "/editor/ckeditor.js")


@api_requests_router.get("/ru.js")
async def get_ru_js(request: Request) -> Response:
    return FileResponse(templates_path + "/editor/ru.js")


@api_requests_router.get("/sport_sections")
async def get_sport_sections(_request: Request) -> list | None:
    try:
        sport_adapter = app_container.get(SportAdapter)
        sport_sections = await sport_adapter.get_sport_list()
    except BaseException as exc:
        logging.warning(exc)
        return None
    return sport_sections


@api_requests_router.get("/activities")
async def get_activities_by_sport_section_id(
    _request: Request, sport_section_id: int
) -> list[Activity] | None:
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        activities = await activity_adapter.get_activities_by_sport_section(
            sport_section_id
        )
    except BaseException as exc:
        logging.warning(exc)
        return None
    return activities


# @api_requests_router.get("/activity")
# async def get_activities_by_sport_section_id(
#     _request: Request,
#     activity_id: int
# ) -> list[Activity] | None:
#     try:
#         activity_adapter = app_container.get(ActivityAdapter)
#         activities = await activity_adapter.get_teams_by_activity_id(activity_id)
#     except BaseException as exc:
#         logging.warning(exc)
#         return None
#     return activities


@api_requests_router.get("/teams")
async def get_teams_by_activity_id(
    _request: Request, activity_id: int
) -> list[Team] | None:
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        teams = await activity_adapter.get_teams_by_activity_id(activity_id)
    except BaseException as exc:
        logging.warning(exc)
        return None
    return teams
