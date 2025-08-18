import uvicorn
from fastapi import FastAPI

from lkshmatch.website.auth.auth import auth_router
from lkshmatch.website.auth.login_middleware import LoginWallMiddleware
from lkshmatch.website.activities import activities_router
from lkshmatch.website.activities_gsheets import table_adapter_router

from lkshmatch.config import settings

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(table_adapter_router, prefix="/table")
app.include_router(activities_router, prefix="")

app.add_middleware(LoginWallMiddleware)

WEBSITE_IP = settings.get("WEBSITE_IP")
WEBSITE_PORT = settings.get("WEBSITE_PORT")

if __name__ == "__main__":
    print("RUN WEBAPP")
    uvicorn.run(app, host=WEBSITE_IP, port=WEBSITE_PORT)
