from dishka.integrations.fastapi import FromDishka, inject

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt

from adapters.core import GetPlayersBySportSections, GetSportSections

root_router = APIRouter()
templates = Jinja2Templates("./webapp/templates")

class User:
    username: str


@root_router.get("/")
async def root(request: Request, username: str = "UU"):
    return templates.TemplateResponse(
        name="index.html", context={"request": request, "username": username}
    )


@root_router.get("/sections")
@inject
async def sections(
    request: Request,
    get_sections: FromDishka[GetSportSections],
):
    return templates.TemplateResponse(
        name="sections.html",
        context={
            "request": request,
            "list_of_sections": await get_sections.get_sections(),
        },
    )


@root_router.get("/sections/{section_name}")
@inject
async def get_list(
    request: Request,
    section_name,
    get_players_by_sport_sections: FromDishka[GetPlayersBySportSections],
    username: str = "UU",
):
    return templates.TemplateResponse(
        name="one_section.html",
        context={
            "request": request,
            "list_of_players": await get_players_by_sport_sections.get_players_by_sport_sections(
                section_name
            ),
            "section_name": section_name,
            "username": username,
        },
    )


@root_router.get("/sections/{section_name}/reg")
async def registration(
    request: Request, section_name: str
):
    # user registration
    return RedirectResponse("/sections/" + section_name)