from dishka.integrations.fastapi import FromDishka, inject

# from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt

from lkshmatch.adapters.sport_sections import GetPlayersBySportSections, GetSportSections

from .auth import auth_router
from .vars import ALGORITHM, COOKIE_NAME, JWT_SECRET_KEY

app = FastAPI()
templates = Jinja2Templates("bff/lkshmatch/webapp/templates")

app.include_router(auth_router, prefix="/auth")


class User:
    username: str


@app.get("/")
async def root(request: Request, username: str = "UU"):
    return templates.TemplateResponse(name="index.html", context={"request": request, "username": username})


@app.get("/sections")
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


@app.get("/sections/{section_name}")
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
            "list_of_players": await get_players_by_sport_sections.get_players_by_sport_sections(section_name),
            "section_name": section_name,
            "username": username,
        },
    )


@app.get("/sections/{section_name}/reg")
async def registration(request: Request, section_name: str):
    # user registration
    return RedirectResponse("/sections/" + section_name)


# @app.get("/sections/{section_name}/reg")
# async def get_list(section_name, user_name, auth):
#     return registration_on_section(section_name, user_name, auth)
# app.add_middleware(TelegramAuth)


@app.middleware("http")
async def dispatch(request: Request, call_next) -> Response:
    if request.url.path.startswith("/auth/"):
        return await call_next(request)

    token = request.cookies.get(COOKIE_NAME)
    login_wall = templates.TemplateResponse("auth/login.html", context={"request": request})
    if not token:
        return login_wall

    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return login_wall

    return await call_next(request)
