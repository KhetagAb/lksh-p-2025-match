from collections.abc import AsyncGenerator

import uvicorn
import uvloop
from fastapi import FastAPI

from lkshmatch.config import settings
from lkshmatch.tg_bot.bot import token, bot, router as bot_router
from lkshmatch.website.activities import activities_router
from lkshmatch.website.activities_gsheets import table_adapter_router
from lkshmatch.website.auth.auth import auth_router
from lkshmatch.website.auth.login_middleware import LoginWallMiddleware


async def lifespan(app: FastAPI) -> AsyncGenerator:
    await bot.remove_webhook()
    await bot.set_webhook(url=f"{settings.get('BASE_URL')}/bot/{token}")
    yield
    await bot.remove_webhook()


def start() -> None:
    uvloop.install()
    app = FastAPI(
        title="Match REST API",
        summary="REST API documentation for Match",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(activities_router)
    app.include_router(auth_router, prefix="/auth")
    app.include_router(table_adapter_router, prefix="/table")
    app.include_router(bot_router, prefix="/bot")

    app.add_middleware(LoginWallMiddleware)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_config="logging.ini",
        log_level="info",
    )


if __name__ == "__main__":
    start()
