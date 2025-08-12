from dishka.integrations.fastapi import FromDishka, inject

from fastapi import APIRouter, Body, Form
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Annotated

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from urllib.parse import urlparse, parse_qs

from bff.lkshmatch.adapters.core import RegisterPlayerInSpotrSection, UnknownError, SportSection, PlayerRegisterInfo

from .vars import CREDENTIALS_FILE, SERVICE_ACCOUNT_NAME

class TableIsEmptyError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Table is empty'

class RegisterInSectionInfo(BaseModel):
    table_url: str
    section_name: str

templates = Jinja2Templates("bff/lkshmatch/webapp/templates")
table_adapter_router = APIRouter()
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http = httpAuth)

def get_sheet_data_from_url(sheet_url: str):
    parse_result = urlparse(sheet_url)
    sheetId = int(parse_qs(parse_result.query)['gid'][0])
    spreadsheetId = parse_result.path.split('/')[3]
    spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
    sheetList = spreadsheet.get('sheets')
    sheetName = None
    for d in sheetList:
        if d['properties']['sheetId'] == sheetId:
            sheetName = d['properties']['title']
            break
    if sheetName is None:
        raise UnknownError
    return {
        'spreadsheetId': spreadsheetId,
        'sheetName': sheetName
    }

@table_adapter_router.get('/register_in_section')
@inject
async def register_on_section_with_table_get(request: Request):
    return templates.TemplateResponse(context={
        'request': request,
        'error': '',
        'service_account_name': SERVICE_ACCOUNT_NAME,
        'username': 'UU'
    }, name='table/register_in_section.html')

@table_adapter_router.post('/register_in_section')
@inject
async def register_on_section_with_table_post(
    request: Request,
    register_player_in_sport_section: FromDishka[RegisterPlayerInSpotrSection],
    table_url: Annotated[str, Form()],
    section_name: Annotated[str, Form()]
):
    error = ''
    try: 
        sheet_data = get_sheet_data_from_url(table_url)
        spreadsheetId = sheet_data['spreadsheetId']
        sheetName = sheet_data['sheetName']
    except BaseException:
        error = 'Неправильная ссылка на таблицу'

    if error == '':
        sheet_values = [ [] ]
        try:
            results = service.spreadsheets().values().get(spreadsheetId = spreadsheetId, 
                                            range=sheetName+"!A1:A1000", majorDimension='COLUMNS').execute()
            if 'values' not in results:
                raise TableIsEmptyError
            sheet_values = results['values'][0]
        except TableIsEmptyError:
            error = 'Таблица пуста'
        except BaseException:
            error = 'Ошибка при загрузке таблицы'
    
    if error == '':
        return_values = [ '' for i in range(len(sheet_values)) ]
        for i in range(len(sheet_values)):
            try:
                await register_player_in_sport_section.register_player_in_sport_section(SportSection(section_name, section_name), 
                                                                                  PlayerRegisterInfo(name=sheet_values[i], id=42))
                return_values[i] = 'Зарегестрирован'
            except BaseException:
                return_values[i] = 'ОШИБКА'
                error = 'Возникли ошибки при регистрации'

        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": sheetName+"!A1:B1000",
                "majorDimension": "COLUMNS",
                "values": [sheet_values, return_values]}
            ]
        }).execute()

    return templates.TemplateResponse(context={
        'request': request,
        'error': error,
        'service_account_name': SERVICE_ACCOUNT_NAME,
        'username': 'UU'
    }, name='table/register_in_section.html')



# sheet_url = 'https://docs.google.com/spreadsheets/d/1bR5o4IVU3RNWPiFA2pq0Wivm5hTxPdkK1FBq8XF04Qo/edit?pli=1&gid=1017497761#gid=1017497761'
# sheet_data = get_sheet_data_from_url(sheet_url)
# spreadsheetId = sheet_data['spreadsheetId']
# sheetName = sheet_data['sheetName']

# results = service.spreadsheets().values().get(spreadsheetId = spreadsheetId, 
#                                      range=sheetName+"!A1:D4").execute() 
# sheet_values = results['values']
# print(sheet_values)

# results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
#     "valueInputOption": "USER_ENTERED",
#     "data": [
#         {"range": sheetName+"!B2:C3",
#          "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
#          "values": [["This is B2", "This is C2"], ["This is B3", "This is C3"]]}
#     ]
# }).execute()