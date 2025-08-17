import asyncio
import uvloop

import uvicorn
from fastapi import FastAPI

from lkshmatch.tg_bot.bot import bot


async def start_app() -> None:
    app = FastAPI(
        title="Match REST API",
        summary="REST API documentation for Match",
        version="0.1.0",
        redoc_url="/",
    )
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


async def start() -> ...:
    uvloop.install()
    loop = asyncio.get_event_loop()

    await loop.run_in_executor(None, bot.polling(none_stop=True), 1)
    await start_app()


if __name__ == "__main__":
    asyncio.run(start())
