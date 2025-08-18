import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from lkshmatch.di import WEBSITE_IP, WEBSITE_PORT
from bff.lkshmatch.website.auth.auth import auth_router
from bff.lkshmatch.website.auth.login_middleware import LoginWallMiddleware
from lkshmatch.website.activities import activities_router
from lkshmatch.website.table_adapter import table_adapter_router


templates = Jinja2Templates("./lkshmatch/website/templates")
app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(table_adapter_router, prefix="/table")
app.include_router(activities_router, prefix="")

app.add_middleware(LoginWallMiddleware)

if __name__ == "__main__":
    print("RUN WEBAPP")
    uvicorn.run(app, host=WEBSITE_IP, port=WEBSITE_PORT)
