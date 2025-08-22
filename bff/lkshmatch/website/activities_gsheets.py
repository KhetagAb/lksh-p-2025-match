from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import Response

from lkshmatch.adapters.base import ActivityAdminAdapter, PlayerAdapter
from lkshmatch.adapters.gheets.gsheets import (
    WEBSITE_SERVICE_ACCOUNT_NAME,
    GSheetDoesNotResponseError,
    change_data_gsheet,
    get_data_gsheet,
    get_sheet_data_from_url,
)
from lkshmatch.di import app_container
from lkshmatch.website.auth.auth import COOKIE_NAME, get_user_id_from_token
from lkshmatch.website.templating import templates


class TableIsEmptyError(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Table is empty"


table_adapter_router = APIRouter(prefix="/table")


@table_adapter_router.get("/register_in_section")
async def register_on_section_with_table_get(request: Request) -> Response:
    return templates.TemplateResponse(
        context={
            "request": request,
            "error": "",
            "service_account_name": WEBSITE_SERVICE_ACCOUNT_NAME,
        },
        name="table/register_in_section.html",
    )


@table_adapter_router.post("/register_in_section")
async def register_on_section_with_table_post(
    request: Request,
    table_url: Annotated[str, Form()],
    activity_id: Annotated[int, Form()],
) -> Response:
    _admin_activity_adapter = app_container.get(ActivityAdminAdapter)
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
                # await admin_activity_adapter.
                return_values[i] = "Зарегестрирован"
            except BaseException:
                return_values[i] = "ОШИБКА"
                error = "Возникли ошибки при регистрации"

        try:
            change_data_gsheet(sheet_data, "B1:B1000", [return_values])  # pyright: ignore[reportPossiblyUnboundVariable]
        except GSheetDoesNotResponseError:
            error = "Возникли проблемы со связью с google-sheets"

    return templates.TemplateResponse(
        context={
            "request": request,
            "error": error,
            "service_account_name": WEBSITE_SERVICE_ACCOUNT_NAME,
        },
        name="table/register_in_section.html",
    )
