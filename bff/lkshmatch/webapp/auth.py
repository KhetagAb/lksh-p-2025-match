import hmac
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from jose import jwt

from .vars import ALGORITHM, BOT_TOKEN_HASH, COOKIE_NAME, JWT_SECRET_KEY

auth_router = APIRouter()


@auth_router.get("/telegram-callback")
async def telegram_callback(
    request: Request,
    user_id: Annotated[int, Query(alias="id")],
    query_hash: Annotated[str, Query(alias="hash")],
):
    params = request.query_params.items()
    data_check_string = "\n".join(sorted(f"{x}={y}" for x, y in params if x not in ("hash", "next")))
    computed_hash = hmac.new(BOT_TOKEN_HASH.digest(), data_check_string.encode(), "sha256").hexdigest()
    is_correct = hmac.compare_digest(computed_hash, query_hash)
    if not is_correct:
        return PlainTextResponse("Authorization failed. Please try again", status_code=401)

    token = jwt.encode(claims={"user_id": user_id}, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    response = RedirectResponse("/")
    response.set_cookie(key=COOKIE_NAME, value=token)
    return response


@auth_router.get("/logout")
async def logout():
    response = RedirectResponse("/")
    response.delete_cookie(key=COOKIE_NAME)
    return response
