import asyncio

import uvicorn
import uvloop
from fastapi import FastAPI

from lkshmatch.tg_bot.bot import router as bot_router
from lkshmatch.webapp.auth import auth_router
from lkshmatch.webapp.login_wall import LoginWallMiddleware
from lkshmatch.webapp.root import root_router
from lkshmatch.webapp.table_adapter import table_adapter_router


async def start() -> ...:
    uvloop.install()

    app = FastAPI(
        title="Match REST API",
        summary="REST API documentation for Match",
        version="0.1.0",
        redoc_url="/",
    )
    app.include_router(auth_router, prefix="/auth")
    app.include_router(table_adapter_router, prefix="/table")
    app.include_router(root_router, prefix="")
    app.include_router(bot_router)

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


if __name__ == "__main__":
    asyncio.run(start())
