from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI

from ..di import all_providers
from lkshmatch.webapp.auth import auth_router
from lkshmatch.webapp.root import root_router
from lkshmatch.webapp.table_adapter import table_adapter_router

import uvicorn

app = FastAPI()
container = make_async_container(*all_providers())
setup_dishka(container, app)

app.include_router(auth_router, prefix="/auth")
app.include_router(table_adapter_router, prefix="/table")
app.include_router(root_router, prefix="")

if __name__ == "__main__":
    print("RUN WEBAPP")
    uvicorn.run(app, host="0.0.0.0", port=80)