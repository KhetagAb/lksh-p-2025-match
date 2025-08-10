from bff.lkshmatch.webapp.vars import JWT_SECRET_KEY, COOKIE_NAME, ALGORITHM
from bff.lkshmatch.webapp.auth import auth_router
from bff.lkshmatch.adapters.rest import RestGetSportSections, RestGetPlayersBySportSections

from jose import JWTError, jwt

# from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response

app = FastAPI()
templates = Jinja2Templates('bff/app/templates')
#static_files = HTMLStaticFiles(directory='site/')

app.include_router(auth_router, prefix="/auth")
#app.mount('/', static_files, name='static')

get_sections = RestGetSportSections()
list_from_sections = RestGetPlayersBySportSections()

# await add_user.add_user(user=PlayerAddInfo("lol"))

class User:
    username: str

@app.get("/")
async def root(request: Request, username: str = "UU"):
    return templates.TemplateResponse(name='index.html',
                                      context={'request': request,
                                               'username': username})

@app.get("/sections")
async def sections(request: Request, username: str = "UU"):
    return templates.TemplateResponse(name='sections.html',
                                      context={'request': request,
                                               'list_of_sections': await get_sections.get_sections(),
                                               'username': username})

@app.get("/sections/{section_name}")
async def get_list(request: Request, section_name, username: str = "UU"):
    return templates.TemplateResponse(name='one_section.html',
                                      context={'request': request,
                                               'list_of_players': await list_from_sections.list_from_sections(section_name),
                                               'section_name': section_name,
                                               'username': username})

@app.get("/sections/{section_name}/reg")
async def registration(request: Request, section_name : str, username: str = "UU"):
    # user registration
    return RedirectResponse("/sections/" + section_name)

# @app.get("/sections/{section_name}/reg")
# async def get_list(section_name, user_name, auth):
#     return registration_on_section(section_name, user_name, auth)
# app.add_middleware(TelegramAuth)

@app.middleware("http")
async def dispatch(request: Request, call_next) -> Response:
    if request.url.path.startswith('/auth/'):
        return await call_next(request)

    token = request.cookies.get(COOKIE_NAME)
    login_wall = templates.TemplateResponse('auth/login.html',
                                          context={'request': request})
    if not token:
        return login_wall

    try:
        token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return login_wall

    user_id = token_parts['user_id']

    return await call_next(request)