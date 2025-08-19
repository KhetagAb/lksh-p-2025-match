from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import Response

from lkshmatch.adapters.base import ActivityAdapter, SportAdapter, PlayerAdapter
from lkshmatch.adapters.gheets.gsheets import (
    get_data_gsheet, change_data_gsheet,
    WEBSITE_SERVICE_ACCOUNT_NAME, get_sheet_data_from_url,
    GSheetDoesNotResponseError
)

from lkshmatch.di import app_container

from lkshmatch.website.templating import templates
from lkshmatch.website.auth.auth import get_user_id_from_token, COOKIE_NAME


class TableIsEmptyError(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Table is empty"


table_adapter_router = APIRouter()

@table_adapter_router.get("/get_sport_sections")
async def get_sport_sections_json(_request: Request) -> list | None:
    try:
        sport_adapter = app_container.get(SportAdapter)
        sport_sections = await sport_adapter.get_sport_list()
    except BaseException:
        return None
    return sport_sections


@table_adapter_router.get("/get_activity_by_sport_section")
async def get_activity_by_sport_section_json(
    _request: Request,
    sport_section_id: int
) -> list | None:
    try:
        activity_adapter = app_container.get(ActivityAdapter)
        activities = await activity_adapter.get_activities_by_sport_section(sport_section_id)
    except BaseException:
        return None
    return activities


@table_adapter_router.get("/register_in_section")
async def register_on_section_with_table_get(request: Request) -> Response:
    return templates.TemplateResponse(
        context={"request": request, "error": "", "service_account_name": WEBSITE_SERVICE_ACCOUNT_NAME},
        name="table/register_in_section.html",
    )


@table_adapter_router.post("/register_in_section")
async def register_on_section_with_table_post(
    request: Request,
    table_url: Annotated[str, Form()],
    activity_id: Annotated[int, Form()],
) -> Response:
    print("table_url:", table_url)
    print("activity_id:", activity_id)
    _activity_adapter = app_container.get(ActivityAdapter)
    _player_adapter = app_container.get(PlayerAdapter)
    cookie_token = request.cookies.get(COOKIE_NAME)
    # TODO: what if cookie_token haven't provided
    _user_id = get_user_id_from_token(cookie_token if cookie_token is not None else "")
    error = ""
    try:
        sheet_data = get_sheet_data_from_url(table_url)
    except GSheetDoesNotResponseError:
        error = "Возникли проблемы со связью с google-sheets"
    except BaseException:
        error = "Неправильная ссылка на таблицу"

    if error == "":
        sheet_values: list = [[]]
        try:
            results = get_data_gsheet(sheet_data, "A1:A1000")
            if "values" not in results:
                raise TableIsEmptyError
            sheet_values = results["values"][0]
        except GSheetDoesNotResponseError:
            error = "Возникли проблемы со связью с google-sheets"
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

        try:
            change_data_gsheet(sheet_data, "B1:B1000", [return_values]) # pyright: ignore[reportPossiblyUnboundVariable]
        except GSheetDoesNotResponseError:
            error = "Возникли проблемы со связью с google-sheets"

    return templates.TemplateResponse(
        context={"request": request, "error": error, "service_account_name": WEBSITE_SERVICE_ACCOUNT_NAME, "username": "UU"},
        name="table/register_in_section.html",
    )
