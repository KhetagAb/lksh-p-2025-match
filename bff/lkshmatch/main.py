import asyncio
from collections.abc import AsyncGenerator

import uvicorn
import uvloop
import os
from fastapi import FastAPI

from lkshmatch.tg_bot.bot import token, bot
from lkshmatch.website.auth.auth import auth_router
from lkshmatch.website.auth.login_middleware import LoginWallMiddleware
from lkshmatch.website.activities_gsheets import table_adapter_router
from lkshmatch.config import settings


async def lifespan(app: FastAPI) -> AsyncGenerator[FastAPI]:
    _remove_webhook = await bot.remove_webhook()
    _set_webhook = await bot.set_webhook(url=os.path.join(settings.get("BASE_URL"), f"bot/{token}")) 
    yield app
    _remove_webhook = await bot.remove_webhook()


async def start() -> None:
    uvloop.install()

    app = FastAPI(
        title="Match REST API",
        summary="REST API documentation for Match",
        version="0.1.0",
        redoc_url="/",
        lifespan=lifespan, # type: ignore
    )
    app.include_router(auth_router, prefix="/auth")
    app.include_router(table_adapter_router, prefix="/table")

    app.add_middleware(LoginWallMiddleware)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["."],
        log_config="../logging.ini",
        log_level="DEBUG",
        env_file="../.env",
    )

    asyncio.run(bot.polling(none_stop=True))


if __name__ == "__main__":
    asyncio.run(start())
