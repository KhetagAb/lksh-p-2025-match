from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI

from di import all_providers
from webapp.auth import auth_router
from webapp.root import root_router
from webapp.table_adapter import table_adapter_router

app = FastAPI()
container = make_async_container(*all_providers())
setup_dishka(container, app)

app.include_router(auth_router, prefix="/auth")
app.include_router(table_adapter_router, prefix="/table")
app.include_router(root_router, prefix="")