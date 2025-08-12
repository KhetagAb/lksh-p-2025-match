from fastapi import FastAPI
from lkshmatch.tg_bot.bot import bot as telegram_bot
from lkshmatch.tg_bot.bot import router as bot_router
from lkshmatch.config import settings
import asyncio


def print_loaded_settings():
    print("Loaded settings:")
    for key, value in settings.as_dict().items():
        print(f"{key} = {value!r}")


app = FastAPI()
print_loaded_settings()
asyncio.run(telegram_bot.polling(non_stop=True))