from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
 
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

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(name='index.html',
                                      context={'request': request})

@app.get("/sections")
def sections(request: Request):
    return templates.TemplateResponse(name='sections.html',
                                      context={'request': request,
                                               'list_of_sections': get_list_of_sections_core()})

@app.get("/sections/{section_name}")
def get_list(request: Request, section_name):
    return templates.TemplateResponse(name='one_section.html',
                                      context={'request': request,
                                               'list_of_players': get_list_in_section_core(section_name),
                                               'section_name': section_name})

@app.get("/sections/{section_name}/reg")
def get_list(section_name, user_name, auth):
    return registration_on_section(section_name, user_name, auth)