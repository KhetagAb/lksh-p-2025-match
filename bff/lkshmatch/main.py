import logging

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
import uvloop
import os
from fastapi import FastAPI

from lkshmatch.tg_bot.bot import token, bot, router as bot_router
from lkshmatch.website.api_requests import api_requests_router
from lkshmatch.website.auth.auth import auth_router
from lkshmatch.website.activities import activities_router
from lkshmatch.website.auth.login_middleware import LoginWallMiddleware
from lkshmatch.website.activities_gsheets import table_adapter_router
from lkshmatch.config import settings


def start() -> None:
    uvloop.install()

    logging.basicConfig(level=logging.INFO)

    app = FastAPI(
        title="Match REST API",
        summary="REST API documentation for Match",
        version="0.1.0",
        redoc_url="/docs2",
    )
    app.include_router(activities_router)
    app.include_router(auth_router)
    app.include_router(table_adapter_router)
    app.include_router(api_requests_router)
    app.include_router(bot_router, prefix="/bot")

    app.add_middleware(LoginWallMiddleware)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        # reload=True,
        # reload_dirs=["."],
        # log_config="../logging.ini",
        # log_level="debug",
        env_file="../.env",
    )


if __name__ == "__main__":
    start()
