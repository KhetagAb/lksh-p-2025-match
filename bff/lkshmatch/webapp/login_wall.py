from fastapi import Request
from fastapi.requests import Request
from fastapi.responses import Response
from jose import JWTError, jwt
from mainWebapp import app

from .root import templates
from .vars import ALGORITHM, COOKIE_NAME, JWT_SECRET_KEY


@app.middleware("http")
async def dispatch(request: Request, call_next) -> Response:
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

    user_id = token_parts["user_id"]

    return await call_next(request)
