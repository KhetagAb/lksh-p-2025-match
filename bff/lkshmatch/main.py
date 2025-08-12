import asyncio

from dishka import Container, make_container
from fastapi import FastAPI

from lkshmatch.config import settings
from lkshmatch.di import all_providers
from lkshmatch.tg_bot.bot import bot as telegram_bot


def print_loaded_settings():
    print("Loaded settings:")
    for key, value in settings.as_dict().items():  # type: ignore
        print(f"{key} = {value!r}")


app = FastAPI()
print_loaded_settings()
container: Container = make_container(*all_providers())
asyncio.run(telegram_bot.polling(non_stop=True))
