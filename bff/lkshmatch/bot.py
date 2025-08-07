from fastapi import APIRouter, Request

import lkshmatch.config as config

router = APIRouter()

# bot = Bot(token=config.settings.telegram_token)
# dispatcher = Dispatcher(bot, update_queue=None, workers=0, use_context=True)

# # Register handlers
# # TODO

# @router.post(f"/webhook/{config.settings.telegram_token}")
# async def webhook(request: Request):
#     data = await request.json()
#     update = Update.de_json(data, bot)
#     dispatcher.process_update(update)
#     return {"ok": True}
