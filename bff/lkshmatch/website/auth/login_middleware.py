from fastapi import Request, Response
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable

from lkshmatch.website.templating import templates
from lkshmatch.website.auth.auth import ALGORITHM, COOKIE_NAME, JWT_SECRET_KEY


class LoginWallMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path.startswith("/auth/"):
            return await call_next(request)

        token = request.cookies.get(COOKIE_NAME)
        login_wall = templates.TemplateResponse("auth/login.html", context={"request": request})
        if not token:
            return login_wall

        try:
            token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        except JWTError:
            return login_wall

        if "user_id" not in token_parts:
            return login_wall

        return await call_next(request)
