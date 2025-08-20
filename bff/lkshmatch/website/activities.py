import logging

from typing import Annotated

from fastapi import APIRouter, Response, Request, Form
from fastapi.responses import RedirectResponse

from lkshmatch.adapters.base import SportAdapter, ActivityAdapter, ActivityAdminAdapter
from lkshmatch.di import app_container

from lkshmatch.website.auth.auth import get_user_id_from_token, COOKIE_NAME
from lkshmatch.website.templating import templates

activities_router = APIRouter(prefix="")


@activities_router.get("/")
async def root(request: Request) -> Response:
    return templates.TemplateResponse(
        name="index.html", context={"request": request}
    )

@activities_router.get("/admin")
async def admin_panel(request: Request, error: str = ''):
    return templates.TemplateResponse(
        name="admin_activity_panel.html",
        context={"request": request, "error": error}
    )

@activities_router.get("/sections")
async def get_sport_sections(
    request: Request,
) -> Response:
    sport_adapter = app_container.get(SportAdapter)
    try:
        sport_list = await sport_adapter.get_sport_list()
    except BaseException as exc:
        logging.warning(exc)
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
    except BaseException as exc:
        logging.warning(exc)
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
async def get_teams_by_activity_id(
    request: Request, sport_section_id: int
) -> Response:
    activity_adapter = app_container.get(ActivityAdapter)
    try:
        list_of_activities = await activity_adapter.get_activities_by_sport_section(
            sport_section_id=sport_section_id
        )
    except BaseException as exc:
        logging.warning(exc)
        return templates.TemplateResponse(
            name="some_error.html", context={"request": request}
        )
    return templates.TemplateResponse(
        name="list_of_activities.html",
        context={"request": request, "list_of_activities": list_of_activities},
    )

@activities_router.post("/sections/activities/delete")
async def delete_activity(
    request: Request,
    activity_id: Annotated[int, Form()],
) -> Response:
    cookie_token = request.cookies.get(COOKIE_NAME)
    user_id = get_user_id_from_token(cookie_token if cookie_token is not None else "")
    admin_activity_adapter = app_container.get(ActivityAdminAdapter)
    error = ''
    try:
        await admin_activity_adapter.delete_activity(user_id, activity_id)
    except BaseException as exc:
        logging.warning(exc)
        error = "Какая-то ошибка"
    return RedirectResponse('/admin?error=' + error, status_code=303)

@activities_router.post("/sections/activities/update")
async def update_activity(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    sport_section_id: Annotated[int, Form()],
) -> Response:
    cookie_token = request.cookies.get(COOKIE_NAME)
    user_id = get_user_id_from_token(cookie_token if cookie_token is not None else "")
    admin_activity_adapter = app_container.get(ActivityAdminAdapter)
    error = ''
    try:
        await admin_activity_adapter.update_activity(user_id, title, sport_section_id, user_id, description)
    except BaseException as exc:
        logging.warning(exc)    
        error = "Какая-то ошибка"
    return RedirectResponse('/admin?error=' + error, status_code=303)

@activities_router.post("/sections/activities/create")
async def create_activity(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    sport_section_id: Annotated[int, Form()],
) -> Response:
    cookie_token = request.cookies.get(COOKIE_NAME)
    user_id = get_user_id_from_token(cookie_token if cookie_token is not None else "")
    username = get_user_id_from_token(cookie_token if cookie_token is not None else "")
    admin_activity_adapter = app_container.get(ActivityAdminAdapter)
    error = ''
    try:
        await admin_activity_adapter.create_activity(username, title, sport_section_id, user_id, description)
    except BaseException as exc:
        logging.warning(exc)    
        error = "Какая-то ошибка"
    return RedirectResponse('/admin?error=' + error, status_code=303)