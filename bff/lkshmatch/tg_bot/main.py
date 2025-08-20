import asyncio
from lkshmatch.tg_bot.bot import bot

asyncio.run(bot.polling(non_stop=True))