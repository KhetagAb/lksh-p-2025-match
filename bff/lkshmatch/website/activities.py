from fastapi import APIRouter, Request
from fastapi.responses import Response

from lkshmatch.adapters.base import SportAdapter, ActivityAdapter
from lkshmatch.di import app_container

from lkshmatch.website.templating import templates

activities_router = APIRouter()


@activities_router.get("/")
async def root(request: Request, username: str = "UU") -> Response:
    return templates.TemplateResponse(
        name="index.html", context={"request": request}
    )


@activities_router.get("/sections")
async def get_sport_sections(
    request: Request,
) -> Response:
    sport_adapter = app_container.get(SportAdapter)
    try:
        sport_list = await sport_adapter.get_sport_list()
    except BaseException:
        return templates.TemplateResponse(
            name="some_error.html", context={"request": request}
        )
    return templates.TemplateResponse(
        name="list_of_sections.html",
        context={
            "request": request,
            "list_of_sections": sport_list,
        },
    )


@activities_router.get("/sections/{sport_section_id}")
async def get_activities_by_sport_section_id(
    request: Request,
    sport_section_id: int
) -> Response:
    activity_adapter = app_container.get(ActivityAdapter)
    try:
        list_of_activities = await activity_adapter.get_activities_by_sport_section(sport_section_id=sport_section_id)
    except BaseException:
        return templates.TemplateResponse(
            name="some_error.html", context={'request': request}
        )
    return templates.TemplateResponse(
        name="list_of_activities.html",
        context={
            'request': request,
            'list_of_activities': list_of_activities
        }
    )

@activities_router.get("/sections/activities/{activity_id}")
async def get_teams_by_activity_id(request: Request, sport_section_id: int) -> Response:
    activity_adapter = app_container.get(ActivityAdapter)
    try:
        list_of_activities = await activity_adapter.get_activities_by_sport_section(
            sport_section_id=sport_section_id
        )
    except BaseException:
        return templates.TemplateResponse(
            name="some_error.html", context={"request": request}
        )
    return templates.TemplateResponse(
        name="list_of_activities.html",
        context={"request": request, "list_of_activities": list_of_activities},
    )
