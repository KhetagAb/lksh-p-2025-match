from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from adapters.stub import StubAddUser, StubGetSections, StubListFromSections, PlayerAddInfo
from auth import auth_router
from jose import JWTError, jwt
import urllib
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import hmac
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, RedirectResponse, Response
from jose import jwt

from vars import BOT_TOKEN_HASH, JWT_SECRET_KEY, COOKIE_NAME
from vars import BOT_TOKEN_HASH, JWT_SECRET_KEY, COOKIE_NAME, WHITELIST

app = FastAPI()
templates = Jinja2Templates('src/templates')
#static_files = HTMLStaticFiles(directory='site/')

# app.include_router(auth_router, prefix="/auth")
#app.mount('/', static_files, name='static')

class TelegramAuth(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path.startswith('/auth/'):
            return await call_next(request)

        url_safe_path = urllib.parse.quote(request.url.path, safe='')
        template_context = {'request': request, 'next_path': url_safe_path}
        login_wall = templates.TemplateResponse('login.html', template_context)

        token = request.cookies.get(COOKIE_NAME)
        if not token:
            return login_wall

        try:
            token_parts = jwt.decode(token, JWT_SECRET_KEY)
        except JWTError:
            return login_wall

        user_id = token_parts['user_id']
        if user_id not in WHITELIST:
            return login_wall

        return await call_next(request)


@app.middleware('http')
async def middleware(request: Request, call_next):
    print("MIDDLEWARE")
    response = await call_next(request)
    if request.url.path.startswith('/auth/'):
        return response

    url_safe_path = urllib.parse.quote(request.url.path, safe='')
    template_context = {'request': request, 'next_path': url_safe_path}
    login_wall = templates.TemplateResponse('login.html', template_context)

    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return login_wall

    try:
        token_parts = jwt.decode(token, JWT_SECRET_KEY)
    except JWTError:
        return login_wall

    user_id = token_parts.claims['k']
    if user_id not in WHITELIST:
        return login_wall

    return response

app = FastAPI()
templates = Jinja2Templates(directory='templates')

def get_list_of_sections_core():
    return ['1', '2', 'hahaha', 'djhs']

def get_list_in_section_core(section: str):
    if section == "1":
        return ["187", "236712738", "237612983"]
    elif section == "2":
        return []
    elif section == "hahaha":
        return ["hahahahaa"]
    else:
        return ["unsigned section"]

def registration_on_section(section_name, user_name, auth):
    return "OK"

def check_telegram_code(username: str, ):
    # Берём 
    return 904

add_user = StubAddUser()
get_sections = StubGetSections()
list_from_sections = StubListFromSections()

# await add_user.add_user(user=PlayerAddInfo("lol"))

@app.get("/")
async def root(request: Request, username: str = "UU"):
    print("SHDJFU")
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
    return RedirectResponse("/sections/" + section_name + "/?username=" + username)

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(name='login.html',
                                        context={'request': request, "next_path": urllib.parse.quote(request.url.path, safe='')})

@app.post("/login/username")
async def login(request: Request, username: str):
    return templates.TemplateResponse(name='login_form_code.html',
                                        context={'request': request})

@app.post("/login/code")
async def login(request: Request):

    return RedirectResponse("/")

@app.get('/auth/telegram-callback')
async def telegram_callback(
        request: Request,
        user_id: Annotated[int, Query(alias='id')],
        query_hash: Annotated[str, Query(alias='hash')],
        #next_url: Annotated[str, Query(alias='next')] = '/',
):
    print(f"USER AUTHED WITH ID: {user_id}")
    params = request.query_params.items()
    data_check_string = '\n'.join(sorted(f'{x}={y}' for x, y in params if x not in ('hash', 'next')))
    computed_hash = hmac.new(BOT_TOKEN_HASH.digest(), data_check_string.encode(), 'sha256').hexdigest()
    is_correct = hmac.compare_digest(computed_hash, query_hash)
    if not is_correct:
        return PlainTextResponse('Authorization failed. Please try again', status_code=401)

    token = jwt.encode({'alg': 'HS256', 'user_id': user_id}, JWT_SECRET_KEY)
    response = RedirectResponse("/")
    response.set_cookie(key=COOKIE_NAME, value=token)
    return response

# @app.get("/sections/{section_name}/reg")
# async def get_list(section_name, user_name, auth):
#     return registration_on_section(section_name, user_name, auth)
app.add_middleware(TelegramAuth)