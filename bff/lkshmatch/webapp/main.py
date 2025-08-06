from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from adapters.stub import StubAddUser, StubGetSections, StubListFromSections, PlayerAddInfo


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

add_user = StubAddUser()
get_sections = StubGetSections()
list_from_sections = StubListFromSections()


# await add_user.add_user(user=PlayerAddInfo("lol"))

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
    return RedirectResponse("/sections/" + section_name + "/?username=" + username)

@app.get("/login")
async def login(request: Request, username: str = "UU"):
    if username == "UU":
        return templates.TemplateResponse(name='login_form.html',
                                          context={'request': request})
    await add_user.add_user(PlayerAddInfo(username))
    return RedirectResponse("/?username="+username)


# @app.get("/sections/{section_name}/reg")
# async def get_list(section_name, user_name, auth):
#     return registration_on_section(section_name, user_name, auth)