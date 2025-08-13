from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from lkshmatch.adapters.base import PlayerAdapter

root_router = APIRouter()
templates = Jinja2Templates("./lkshmatch/webapp/templates")


class User:
    username: str


@root_router.get("/")
async def root(request: Request, username: str = "UU"):
    return templates.TemplateResponse(name="index.html", context={"request": request, "username": username})


# @root_router.get("/sections")
# @inject
# async def sections(
#     request: Request,
#     player_adapter: FromDishka[PlayerAdapter],
# ):
#     return templates.TemplateResponse(
#         name="sections.html",
#         context={
#             "request": request,
#             "list_of_sections": await player_adapter.get_sections(),
#         },
#     )


# @root_router.get("/sections/{section_name}")
# @inject
# async def get_list(
#     request: Request,
#     section_name,
#     get_players_by_sport_sections: FromDishka[GetPlayersBySportSections],
#     username: str = "UU",
# ):
#     return templates.TemplateResponse(
#         name="one_section.html",
#         context={
#             "request": request,
#             "list_of_players": await get_players_by_sport_sections.get_players_by_sport_sections(section_name),
#             "section_name": section_name,
#             "username": username,
#         },
#     )


# @root_router.get("/sections/{section_name}/reg")
# async def registration(request: Request, section_name: str):
#     # user registration
#     return RedirectResponse("/sections/" + section_name)
