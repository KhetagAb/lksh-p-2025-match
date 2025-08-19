from fastapi import FastAPI
import uvicorn
import logging

from lkshmatch.website.api_requests import api_requests_router
from lkshmatch.website.auth.auth import auth_router
from lkshmatch.website.activities import activities_router
from lkshmatch.website.auth.login_middleware import LoginWallMiddleware
from lkshmatch.website.activities_gsheets import table_adapter_router

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

app.add_middleware(LoginWallMiddleware)

uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8000,
    env_file="../.env",
)