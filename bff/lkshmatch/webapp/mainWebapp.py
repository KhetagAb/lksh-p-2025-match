import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from lkshmatch.di import app_container
from lkshmatch.webapp.auth import auth_router
from lkshmatch.webapp.login_wall import LoginWallMiddleware
from lkshmatch.webapp.root import root_router
from lkshmatch.webapp.table_adapter import table_adapter_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(table_adapter_router, prefix="/table")
app.include_router(root_router, prefix="")

app.add_middleware(LoginWallMiddleware)

if __name__ == "__main__":
    print("RUN WEBAPP")
    uvicorn.run(app, host="0.0.0.0", port=80)
