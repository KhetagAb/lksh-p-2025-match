from fastapi import FastAPI
from app.bot import router as bot_router
from app.config import settings


def print_loaded_settings():
    print("Loaded settings:")
    for key, value in settings.as_dict().items():
        print(f"{key} = {value!r}")


app = FastAPI()
print_loaded_settings()
