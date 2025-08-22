import hashlib
import hmac
from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse, RedirectResponse, Response
from jose import jwt

from lkshmatch.di import settings

JWT_SECRET_KEY = settings.get("WEBSITE_JWT_SECRET_KEY")
BOT_TOKEN_HASH = hashlib.sha256(settings.get("WEBSITE_TELEGRAM_TOKEN").encode())
COOKIE_NAME = "auth-token"
ALGORITHM = "HS256"

auth_router = APIRouter(prefix="/auth")


def get_user_id_from_token(token: str) -> int:
    token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return int(token_parts["user_id"])

def get_username_from_token(token: str) -> str:
    token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return token_parts["username"]


def get_username_from_token(token: str) -> str:
    token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return token_parts["username"]


# Код взят из https://github.com/tm-a-t/telegram-auth-wall
@auth_router.get("/telegram-callback")
async def telegram_callback(
    request: Request,
    user_id: Annotated[int, Query(alias="id")],
    username: Annotated[str, Query(alias="username")],
    query_hash: Annotated[str, Query(alias="hash")],
) -> Response:
    params = request.query_params.items()
    data_check_string = "\n".join(
        sorted(f"{x}={y}" for x, y in params if x not in ("hash", "next"))
    )
    computed_hash = hmac.new(
        BOT_TOKEN_HASH.digest(), data_check_string.encode(), "sha256"
    ).hexdigest()
    is_correct = hmac.compare_digest(computed_hash, query_hash)
    if not is_correct:
        return PlainTextResponse(
            "Authorization failed. Please try again", status_code=401
        )

    token = jwt.encode(
        claims={"user_id": user_id, "username": username},
        key=JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = RedirectResponse("/")
    response.set_cookie(key=COOKIE_NAME, value=token)
    return response


@auth_router.get("/logout")
async def logout() -> Response:
    response = RedirectResponse("/")
    response.delete_cookie(key=COOKIE_NAME)
    return response
