from urllib.parse import urlparse, parse_qs
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from lkshmatch.config import settings

WEBSITE_CREDENTIALS_FILE: str | None = settings.get(
    "WEBSITE_CREDENTIALS_FILE"
)
WEBSITE_SERVICE_ACCOUNT_NAME: str | None = settings.get(
    "WEBSITE_SERVICE_ACCOUNT_NAME"
)  # почта сервисного аккаунта
service = None
try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        WEBSITE_CREDENTIALS_FILE,
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build("sheets", "v4", http=httpAuth)
except BaseException:
    print("Problems with gsheets")

class GSheetDoesNotResponseError(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "GSheet does not response"

class GSheetData:
    def __init__(self, spreadsheetId: str, sheetName: str):
        self.spreadsheetId = spreadsheetId
        self.sheetName = sheetName


def get_sheet_data_from_url(sheet_url: str) -> GSheetData:
    parse_result = urlparse(sheet_url)
    sheetId = int(parse_qs(parse_result.query)["gid"][0])
    spreadsheetId = parse_result.path.split("/")[3]

    if service is None:
        raise GSheetDoesNotResponseError

    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    except BaseException:
        raise GSheetDoesNotResponseError
    
    sheetList = spreadsheet.get("sheets")
    sheetName = None
    for d in sheetList:
        if d["properties"]["sheetId"] == sheetId:
            sheetName = d["properties"]["title"]
            break
    if sheetName is None:
        raise
    return GSheetData(spreadsheetId, sheetName)


def get_data_gsheet(sheet_data: GSheetData, range: str, mod: str = "COLUMNS") -> list[list[str]]:
    # mod shoud be "ROWS" or "COLUMNS"
    if service is None:
        raise GSheetDoesNotResponseError

    try:
        results = service.spreadsheets().values().get(
                spreadsheetId=sheet_data.spreadsheetId,
                range=sheet_data.sheetName + "!" + range,
                majorDimension=mod,
            ).execute()
    except BaseException:
        raise GSheetDoesNotResponseError
    
    return results


def change_data_gsheet(
    sheet_data: GSheetData, range: str, data: list[list[str]], mod: str = "COLUMNS"
) -> list[list[str]]:
    if service is None:
        raise GSheetDoesNotResponseError
    
    try:
        # mod shoud be "ROWS" or "COLUMNS"
        results = (
            service.spreadsheets()
            .values()
            .batchUpdate(
                spreadsheetId=sheet_data.spreadsheetId,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {
                            "range": sheet_data.sheetName + "!" + range,
                            "majorDimension": "COLUMNS",
                            "values": data,
                        }
                    ],
                },
            )
            .execute()
        )
    except BaseException:
        raise GSheetDoesNotResponseError
    
    return results
