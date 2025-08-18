from typing import Annotated
from urllib.parse import parse_qs, urlparse

from fastapi import APIRouter, Form, Request

from lkshmatch.adapters.base import ActivityAdapter, SportAdapter, PlayerAdapter
from lkshmatch.di import app_container, service
from lkshmatch.website.main import templates

from lkshmatch.website.auth.auth import get_user_id_from_token, COOKIE_NAME
from lkshmatch.di import WEBSITE_SERVICE_ACCOUNT_NAME


class TableIsEmptyError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "Table is empty"


def get_sheet_data_from_url(sheet_url: str):
    parse_result = urlparse(sheet_url)
    sheetId = int(parse_qs(parse_result.query)["gid"][0])
    spreadsheetId = parse_result.path.split("/")[3]
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheetList = spreadsheet.get("sheets")
    sheetName = None
    for d in sheetList:
        if d["properties"]["sheetId"] == sheetId:
            sheetName = d["properties"]["title"]
            break
    if sheetName is None:
        raise
    return {"spreadsheetId": spreadsheetId, "sheetName": sheetName}


table_adapter_router = APIRouter()

@table_adapter_router.get("/get_sport_sections")
async def get_sport_sections_json(request: Request):
    try:
        sport_adapter = app_container.get(SportAdapter)
        sport_sections = await sport_adapter.get_sport_list()
    except:
        return None
    return sport_sections


@table_adapter_router.get("/get_activity_by_sport_section")
async def get_activity_by_sport_section_json(
    request: Request,
    sport_section_id: int
):
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        activities = await activity_adapter.get_activities_by_sport_section(sport_section_id)
    except:
        return None
    return activities


@table_adapter_router.get("/register_in_section")
async def register_on_section_with_table_get(request: Request):
    return templates.TemplateResponse(
        context={"request": request, "error": "", "service_account_name": WEBSITE_SERVICE_ACCOUNT_NAME},
        name="table/register_in_section.html",
    )


@table_adapter_router.post("/register_in_section")
async def register_on_section_with_table_post(
    request: Request,
    table_url: Annotated[str, Form()],
    activity_id: Annotated[int, Form()],
):
    print("table_url:", table_url)
    print("activity_id:", activity_id)
    activity_adapter = app_container.get(ActivityAdapter)
    player_adapter = app_container.get(PlayerAdapter)
    user_id = get_user_id_from_token(request.cookies.get(COOKIE_NAME))
    error = ""
    try:
        sheet_data = get_sheet_data_from_url(table_url)
        spreadsheetId = sheet_data["spreadsheetId"]
        sheetName = sheet_data["sheetName"]
    except BaseException:
        error = "Неправильная ссылка на таблицу"

    if error == "":
        sheet_values = [[]]
        try:
            results = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheetId, range=sheetName + "!A1:A1000", majorDimension="COLUMNS")
                .execute()
            )
            if "values" not in results:
                raise TableIsEmptyError
            sheet_values = results["values"][0]
        except TableIsEmptyError:
            error = "Таблица пуста"
        except BaseException:
            error = "Ошибка при загрузке таблицы"

    if error == "":
        return_values = ["" for i in range(len(sheet_values))]
        for i in range(len(sheet_values)):
            try:
                # await activity_adapter.enroll_player_in_activity(player_tg_id=user_id, activity_id=activity_id)
                return_values[i] = "Зарегестрирован"
            except BaseException:
                return_values[i] = "ОШИБКА"
                error = "Возникли ошибки при регистрации"

        results = (
            service.spreadsheets()
            .values()
            .batchUpdate(
                spreadsheetId=spreadsheetId,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {
                            "range": sheetName + "!A1:B1000",
                            "majorDimension": "COLUMNS",
                            "values": [sheet_values, return_values],
                        }
                    ],
                },
            )
            .execute()
        )

    return templates.TemplateResponse(
        context={"request": request, "error": error, "service_account_name": WEBSITE_SERVICE_ACCOUNT_NAME, "username": "UU"},
        name="table/register_in_section.html",
    )
